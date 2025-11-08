from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name",
            "email",
            "phone_number",
            "street_address1",
            "street_address2",
            "postcode",
            "town_or_city",
            "county",
            "country",
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "street_address1": "Address Line 1",
            "street_address2": "Address Line 2",
            "postcode": "Post Code",
            "town_or_city": "Town or City",
            "county": "County, State or Locality",
        }

        self.fields["full_name"].widget.attrs["autofocus"] = True

        for field in self.fields:
            if field == "country":
                self.fields[field].widget.attrs["class"] = "form-control"
            else:
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
                self.fields[field].widget.attrs["class"] = "form-control"
