from django.test import TestCase
from home.models import ContactMessage


class ContactMessageModelTest(TestCase):
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

    def test_contact_message_name(self):
        """Test the name field"""
        self.assertEqual(self.message.name, "Rafael")

    def test_contact_message_email(self):
        """Test the email field"""
        self.assertEqual(self.message.email, "rafa@example.com")

    def test_contact_message_message(self):
        """Test the message field"""
        self.assertEqual(self.message.message, "This is a test message.")

    def test_contact_message_created_at(self):
        """Test the created_at field"""
        self.assertIsNotNone(self.message.created_at)

    def test_contact_message_ordering(self):
        """Test that messages are ordered by created_at descending"""
        messages = ContactMessage.objects.all()

        # Rafael should be first as it is the oldest.
        print(messages[0])
        self.assertEqual(messages[0], self.message)
        # Gustavo should be second as it is the newest.
        print(messages[1])
        self.assertEqual(messages[1], self.message_2)

    def test_contact_message_verbose_name(self):
        """Test verbose name is set correctly"""
        self.assertEqual(
            str(ContactMessage._meta.verbose_name), "Contact Message"
        )

    def test_contact_message_verbose_name_plural(self):
        """Test verbose name plural is set correctly"""
        self.assertEqual(
            str(ContactMessage._meta.verbose_name_plural), "Contact Messages"
        )

    def test_contact_message_str_method(self):
        """Test string representation of the model"""
        expected = "Message from Rafael, (rafa@example.com)"
        self.assertEqual(str(self.message), expected)
