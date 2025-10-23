from django.shortcuts import render


# Create your views here.
def view_trolley(request):
    """A view to return the trolley page"""
    return render(request, "trolley/trolley.html")
