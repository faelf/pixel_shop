from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm


# Create your views here.
def checkout_view(request):
    """
    A view to handle the checkout page
    """
    trolley = request.session.get("trolley", {})
    if not trolley:
        messages.error(request, "Your trolley is empty")
        return redirect("products_list")

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "trolley": trolley,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": "test_secret",
    }
    return render(request, template, context)
