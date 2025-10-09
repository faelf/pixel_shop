from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm


def home(request):
    return render(request, "home/home.html")


def contact_page(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("home")
    else:
        form = ContactMessageForm()

    return render(request, "home/contact.html", {"form": form})
