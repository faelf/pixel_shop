from django import forms
from allauth.account.forms import LoginForm, SignupForm
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Your Email"}
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Message",
                    "rows": 3,
                }
            ),
        }


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Redefine all fields as self.fields
        self.fields["first_name"] = forms.CharField(
            max_length=30,
            label="First Name",
            widget=forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your first name"}
            ),
        )
        self.fields["last_name"] = forms.CharField(
            max_length=30,
            label="Last Name",
            widget=forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your last name"}
            ),
        )
        self.fields["email"] = forms.EmailField(
            label="Email",
            widget=forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
        )
        self.fields["email2"] = forms.EmailField(
            label="Confirm Email",
            widget=forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Confirm your email"}
            ),
        )
        self.fields["username"] = forms.CharField(
            max_length=150,
            label="Username",
            widget=forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Choose a username"}
            ),
        )
        self.fields["password1"] = forms.CharField(
            label="Password",
            widget=forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Enter your password"}
            ),
        )
        self.fields["password2"] = forms.CharField(
            label="Confirm Password",
            widget=forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Confirm your password"}
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")
        if email and email2 and email != email2:
            raise forms.ValidationError("Email addresses do not match.")
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your username or email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        )
