from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse


# Create your views here.
def view_trolley(request):
    """
    Render the trolley page, extending the base template.
    """
    return render(request, "trolley/trolley.html")


def add_to_trolley(request, item_id):
    """
    Add a quantity of the specified product to the shopping trolley
    """
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    trolley = request.session.get("trolley", {})

    if item_id in list(trolley.keys()):
        trolley[item_id] += quantity
    else:
        trolley[item_id] = quantity

    request.session["trolley"] = trolley
    return redirect(redirect_url)


def update_trolley(request, item_id):
    """
    Update the quantity of the specified product in the shopping trolley.
    """

    if request.method == "POST":
        redirect_url = request.POST.get("redirect_url", reverse("trolley"))
        try:
            quantity = int(request.POST.get("quantity", 0))
        except ValueError:
            quantity = 0

        trolley = request.session.get("trolley", {})

        if quantity > 0:
            trolley[item_id] = quantity
            messages.info(request, "Quantity updated.")
        elif item_id in trolley:
            trolley.pop(item_id)
            messages.success(request, "Item successfully removed from your trolley.")

        request.session["trolley"] = trolley

        return redirect(redirect_url)
    return redirect(reverse("trolley"))


def delete_item_from_trolley(request, item_id):
    """
    Delete an item from the shopping trolley.
    """
    if request.method == "POST":
        trolley = request.session.get("trolley", {})
        item_id_str = str(item_id)
        if item_id_str in trolley:
            trolley.pop(item_id_str)
            messages.success(request, "Item successfully removed from your trolley.")
        request.session["trolley"] = trolley

    return redirect(reverse("trolley"))
