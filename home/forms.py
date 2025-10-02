from allauth.account.forms import LoginForm
from django import forms


class CustomLoginForm(LoginForm):
    login = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your username or email",
            }
        ),
    )
    # username = forms.CharField(
    #     label="Username",
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Enter your username",
    #         }
    #     ),
    # )
    # email = forms.EmailField(
    #     label="Email",
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Enter your username or email",
    #         }
    #     ),
    # )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        ),
    )
