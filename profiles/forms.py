from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        widget_classes = {
            "default_country": "form-select",
        }

        placeholders = {
            "default_phone_number": "Phone Number",
            "default_postcode": "Postcode",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Address Line 1",
            "default_street_address2": "Address Line 2",
            "default_county": "County",
        }

        labels = {
            "default_phone_number": "Phone Number",
            "default_postcode": "Postcode",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Address Line 1",
            "default_street_address2": "Address Line 2",
            "default_county": "County",
            "default_country": "Country",
        }

        for field_name, field in self.fields.items():
            # Apply Classes (form-control as a fallback)
            field.widget.attrs["class"] = widget_classes.get(
                field_name, "form-control"
            )

            # Apply Labels
            if field_name in labels:
                field.label = labels[field_name]

            # Apply Placeholders
            if field_name in placeholders:
                placeholder_text = placeholders[field_name]
                if field.required:
                    placeholder_text = f"{placeholder_text} *"
                field.widget.attrs["placeholder"] = placeholder_text
