from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "categories", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "categories": forms.CheckboxSelectMultiple(),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "categories": "Categories",
        }
