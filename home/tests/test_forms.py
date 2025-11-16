from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm, SignupForm
from django.forms.widgets import TextInput, EmailInput, PasswordInput, Textarea
from home.forms import ContactMessageForm, CustomSignupForm, CustomLoginForm
from home.models import ContactMessage


class ContactMessageFormTest(TestCase):
    def setUp(self):
        self.form = ContactMessageForm()

    def test_form_uses_correct_model(self):
        """Test that form uses ContactMessage model"""
        self.assertEqual(self.form._meta.model, ContactMessage)

    def test_form_has_correct_fields(self):
        """Test that form has the correct fields"""
        # print(form.fields)
        # print(form.fields["name"])
        # print(form.fields["email"])
        # print(form.fields["message"])
        self.assertIn("name", self.form.fields)
        self.assertIn("email", self.form.fields)
        self.assertIn("message", self.form.fields)
        self.assertEqual(len(self.form.fields), 3)

    def test_fields_have_correct_input_type(self):
        """Test if fields have correct input type"""
        self.assertIsInstance(self.form.fields["name"].widget, TextInput)
        self.assertIsInstance(self.form.fields["email"].widget, EmailInput)
        self.assertIsInstance(self.form.fields["message"].widget, Textarea)

    def test_fields_are_required(self):
        """Test if fields are required"""
        self.assertTrue(self.form.fields["name"].required, True)
        self.assertTrue(self.form.fields["email"].required, True)
        self.assertTrue(self.form.fields["message"].required, True)

    def test_form_has_correct_classes(self):
        """Test that fields have correct classes"""
        self.assertEqual(
            self.form.fields["name"].widget.attrs["class"], "form-control"
        )
        self.assertEqual(
            self.form.fields["email"].widget.attrs["class"], "form-control"
        )
        self.assertEqual(
            self.form.fields["message"].widget.attrs["class"], "form-control"
        )

    def test_form_has_placeholders(self):
        """Test that fields have placeholders"""
        self.assertEqual(
            self.form.fields["name"].widget.attrs["placeholder"], "Your Name"
        )
        self.assertEqual(
            self.form.fields["email"].widget.attrs["placeholder"], "Your Email"
        )
        self.assertEqual(
            self.form.fields["message"].widget.attrs["placeholder"],
            "Your Message",
        )

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            "name": "Gustavo",
            "email": "gustavo@example.com",
            "message": "This is a test message 2.",
        }
        form = ContactMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test form with valid data"""
        form_data = {
            "name": "",
            "email": "cristiana",
            "message": "",
        }
        form = ContactMessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("message", form.errors)

    def test_form_saves_correctly(self):
        """Test that form saves data to database correctly"""
        form_data = {
            "name": "Rafael",
            "email": "rafael@example.com",
            "message": "This is a test message.",
        }
        form = ContactMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

        message = form.save()

        self.assertEqual(message.name, "Rafael")
        self.assertEqual(message.email, "rafael@example.com")
        self.assertEqual(message.message, "This is a test message.")
        self.assertIsNotNone(message.created_at)


class CustomLoginFormTest(TestCase):
    def setUp(self):
        self.form = CustomLoginForm()

    def test_form_inherits_from_login_form(self):
        """Test that CustomLoginForm inherits from allauth LoginForm"""
        self.assertIsInstance(self.form, LoginForm)

    def test_login_form_has_correct_fields(self):
        """Test that form has login and password fields"""
        self.assertIn("login", self.form.fields)
        self.assertIn("password", self.form.fields)

    def test_login_form_has_placeholder(self):
        """Test that login field has placeholder text"""
        self.assertEqual(
            self.form.fields["login"].widget.attrs["placeholder"],
            "Enter your username or email",
        )
        self.assertEqual(
            self.form.fields["password"].widget.attrs["placeholder"],
            "Enter your password",
        )

    def test_form_has_form_control_class(self):
        """Test that login field has form-control CSS class"""
        self.assertIn(
            "form-control", self.form.fields["login"].widget.attrs["class"]
        )
        self.assertIn(
            "form-control", self.form.fields["login"].widget.attrs["class"]
        )


class CustomSignupFormTest(TestCase):
    def setUp(self):
        """Create a form instance for each test"""
        self.form = CustomSignupForm()

    def test_form_inherits_from_signup_form(self):
        """Test that CustomSignupForm inherits from allauth SignupForm"""
        self.assertIsInstance(self.form, SignupForm)

    def test_form_has_correct_fields(self):
        """Test that form has the correct fields"""
        self.assertIn("first_name", self.form.fields)
        self.assertIn("last_name", self.form.fields)
        self.assertIn("email", self.form.fields)
        self.assertIn("email2", self.form.fields)
        self.assertIn("username", self.form.fields)
        self.assertIn("password1", self.form.fields)
        self.assertIn("password2", self.form.fields)
        self.assertEqual(len(self.form.fields), 7)

    def test_fields_have_correct_labels(self):
        # print(self.form.fields["first_name"].widget)
        self.assertEqual(
            self.form.fields["first_name"].label,
            "First Name",
        )

    def test_fields_have_correct_input_type(self):
        """Test fields input type"""
        self.assertIsInstance(self.form.fields["first_name"].widget, TextInput)
        self.assertIsInstance(self.form.fields["last_name"].widget, TextInput)
        self.assertIsInstance(self.form.fields["email"].widget, EmailInput)
        self.assertIsInstance(self.form.fields["email2"].widget, EmailInput)
        self.assertIsInstance(self.form.fields["username"].widget, TextInput)
        self.assertIsInstance(
            self.form.fields["password1"].widget, PasswordInput
        )
        self.assertIsInstance(
            self.form.fields["password2"].widget, PasswordInput
        )

    def test_fields_have_correct_classes(self):
        """Test if fields have correct classes"""
        self.assertEqual(
            self.form.fields["first_name"].widget.attrs["class"],
            "form-control",
        )
        self.assertEqual(
            self.form.fields["last_name"].widget.attrs["class"],
            "form-control",
        )
        self.assertEqual(
            self.form.fields["email"].widget.attrs["class"],
            "form-control",
        )
        self.assertEqual(
            self.form.fields["email2"].widget.attrs["class"],
            "form-control",
        )
        self.assertEqual(
            self.form.fields["username"].widget.attrs["class"],
            "form-control",
        )
        self.assertEqual(
            self.form.fields["password1"].widget.attrs["class"],
            "form-control",
        )
        self.assertEqual(
            self.form.fields["password2"].widget.attrs["class"],
            "form-control",
        )

    def test_fields_are_required(self):
        """Test if fields are required"""
        self.assertTrue(self.form.fields["first_name"].required, True)
        self.assertTrue(self.form.fields["last_name"].required, True)
        self.assertTrue(self.form.fields["email"].required, True)
        self.assertTrue(self.form.fields["email2"].required, True)
        self.assertTrue(self.form.fields["username"].required, True)
        self.assertTrue(self.form.fields["password1"].required, True)
        self.assertTrue(self.form.fields["password2"].required, True)

    def test_clean_matching_emails(self):
        """Test that matching emails pass validation"""
        form_data = {
            "username": "rafael",
            "email": "rafa@example.com",
            "email2": "rafa@example.com",
            "first_name": "Rafael",
            "last_name": "Ferreira",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        form = CustomSignupForm(data=form_data)
        # print(f"is valid: {form.is_valid()}")
        self.assertTrue(form.is_valid())

    def test_clean_non_matching_emails(self):
        """Test that non-matching emails raise validation error"""
        form_data = {
            "username": "rafael",
            "email": "rafa@example.com",
            "email2": "fael@example.com",
            "first_name": "Rafael",
            "last_name": "Ferreira",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }
        form = CustomSignupForm(data=form_data)
        # print(f"is valid: {form.is_valid()}")
        self.assertFalse(form.is_valid())

        # print(f"all errors: {form.errors}")
        # print(f"all errors as dict: {form.errors.as_data()}")
        # print(f"non-field errors: {form.non_field_errors()}")
        self.assertIn("email2", form.errors)

    def test_save_user_can_login(self):
        """Test that saved user can authenticate"""

        User = get_user_model()

        form_data = {
            "username": "test_user",
            "email": "test@example.com",
            "email2": "test@example.com",
            "first_name": "Rafael",
            "last_name": "Ferreira",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

        response = self.client.post(
            reverse("account_signup"), data=form_data, follow=True
        )

        # user_exists = User.objects.filter(username="test_user").exists()
        # print(f"User exists: {user_exists}")

        user = User.objects.get(username="test_user")

        authenticated_user = authenticate(
            username="test_user", password="ComplexPass123!"
        )

        # print(f"Response status: {response.status_code}")
        # print(f"Response redirect: {response.redirect_chain}")
        # print(f"User: {user}")
        # print(f"User is active: {user.is_active}")
        # print(f"User has usable password: {user.has_usable_password()}")
        # print(f"Authenticated user: {authenticated_user}")

        self.assertEqual(
            response.redirect_chain, [("/accounts/confirm-email/", 302)]
        )
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, user)
