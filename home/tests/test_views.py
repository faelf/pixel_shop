from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from home.models import ContactMessage
from home.forms import ContactMessageForm


class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        """Test that home page returns 200 status code"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """Test that home view uses the correct template"""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/home.html")

    def test_home_view_uses_base_template(self):
        """Test that home template extends base.html"""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")

    def test_home_view_accessible_by_url(self):
        """Test that home page is accessible by its URL"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class ContactPageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.message = ContactMessage.objects.create(
            name="Rafael",
            email="rafa@example.com",
            message="This is a test message.",
        )
        cls.message_2 = ContactMessage.objects.create(
            name="Gustavo",
            email="gustavo@example.com",
            message="This is a test message.",
        )

    def test_contact_page_status_code(self):
        """Test that contact page returns 200 status code"""
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_uses_correct_template(self):
        """Test that contact view uses the correct template"""
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response, "home/contact.html")

    def test_contact_page_contains_form(self):
        """Test that contact page contains the form"""
        response = self.client.get(reverse("contact"))
        self.assertIsInstance(response.context["form"], ContactMessageForm)

    def test_contact_form_valid_submission(self):
        """Test submitting a valid contact form"""
        form_data = {
            "name": "Cristiana",
            "email": "cristiana@example.com",
            "message": "This is a test message.",
        }
        response = self.client.post(reverse("contact"), data=form_data)

        # Check redirect to home
        self.assertRedirects(response, reverse("home"))

        # Check message was saved (2 + 1)
        self.assertEqual(ContactMessage.objects.count(), 3)
        message = ContactMessage.objects.last()
        self.assertEqual(message.name, "Cristiana")
        self.assertEqual(message.email, "cristiana@example.com")
        self.assertEqual(message.message, "This is a test message.")

        # Check success message
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Message sent successfully!")

    def test_contact_form_invalid_submission(self):
        """Test submitting an invalid contact form"""
        form_data = {
            "name": "",
            "email": "invalid-email",
            "message": "",
        }
        response = self.client.post(reverse("contact"), data=form_data)

        # Should not redirect
        self.assertEqual(response.status_code, 200)

        # Should not save message
        self.assertEqual(ContactMessage.objects.count(), 2)

        # Should return form with errors
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("message", form.errors)

    def test_contact_page_displays_messages_oldest_first(self):
        """Test that messages are ordered by created_at ascending"""
        response = self.client.get(reverse("contact"))
        user_messages = response.context["user_messages"]

        # Rafael should be first as it is the oldest.
        self.assertEqual(user_messages[0].name, self.message.name)
        # Gustavo should be second as it is the newest.
        self.assertEqual(user_messages[1].name, self.message_2.name)

    def test_contact_page_context_contains_user_messages(self):
        """Test that context includes user_messages"""
        response = self.client.get(reverse("contact"))
        self.assertIn("user_messages", response.context)


User = get_user_model()


class DeleteMessageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create_user(
            username="rafael", password="testpass123", is_staff=True
        )
        cls.regular_user = User.objects.create_user(
            username="gustavo", password="testpass123", is_staff=False
        )
        cls.message = ContactMessage.objects.create(
            name="Cristiana",
            email="cristiana@example.com",
            message="Test message to delete",
        )

    def test_delete_message_requires_login(self):
        """Test that delete view requires authentication"""
        response = self.client.post(
            reverse("delete_message", args=[self.message.id])
        )
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_message_requires_staff(self):
        """Test that delete view requires staff permissions"""
        # Login as regular user
        self.client.login(username="gustavo", password="testpass123")

        # print(self.message)
        response = self.client.post(
            reverse("delete_message", args=[self.message.id])
        )

        # Should be denied (302 redirect or 403 forbidden)
        self.assertIn(response.status_code, [302, 403])

        # Message should NOT be deleted
        self.assertTrue(
            ContactMessage.objects.filter(id=self.message.id).exists()
        )

    def test_delete_message_as_staff(self):
        """Test that staff can delete message"""
        # Login as staff
        self.client.login(username="rafael", password="testpass123")

        messages_count = ContactMessage.objects.count()
        # print(messages_count)
        response = self.client.post(
            reverse("delete_message", args=[self.message.id])
        )

        # Should redirect to contact page
        self.assertRedirects(response, reverse("contact"))

        # Message should be deleted
        messages_count = ContactMessage.objects.count()
        # print(messages_count)
        self.assertEqual(messages_count, 0)
        self.assertFalse(
            ContactMessage.objects.filter(id=self.message.id).exists()
        )

        # Should show success message
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn("successfully deleted", str(messages_list[0]))
