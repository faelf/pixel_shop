from django.shortcuts import render, redirect


# Create your views here.
def view_trolley(request):
    """A view to return the trolley page"""
    return render(request, "trolley/trolley.html")


def add_to_trolley(request, item_id):
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    trolley = request.session.get("trolley", {})

    if item_id in list(trolley.keys()):
        trolley[item_id] += quantity
    else:
        trolley[item_id] = quantity

    request.session["trolley"] = trolley
    return redirect(redirect_url)
