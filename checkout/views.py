from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from trolley.contexts import trolley_contents
import stripe


# Create your views here.
def checkout_view(request):
    """
    A view to handle the checkout page
    Payments through Stripe
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        trolley = request.session.get("trolley", {})

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "county": request.POST["county"],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()

            # Create order line items
            for item_id, quantity in trolley.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One of the products in your trolley wasn't found. "
                        "Please contact us for assistance!",
                    )
                    order.delete()
                    return redirect(reverse("view_trolley"))

            # Save the info checkbox preference
            request.session["save_info"] = "save-info" in request.POST
            return redirect(reverse("checkout_success", args=[order.order_number]))
        else:
            messages.error(
                request,
                "There was an error with your form. \
                Please check your information.",
            )

    else:
        trolley = request.session.get("trolley", {})
        if not trolley:
            messages.error(request, "Your trolley is empty")
            return redirect("products_list")

        current_trolley = trolley_contents(request)
        total = current_trolley["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, "Stripe public key is missing.")

        template = "checkout/checkout.html"

        context = {
            "order_form": order_form,
            "trolley": trolley,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
        }
        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get("save_info")
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(
        request,
        f"Order successfully processed! \
        A confirmation email will be sent to {order.email}.",
    )

    if "trolley" in request.session:
        del request.session["trolley"]

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
    }
    return render(request, template, context)
