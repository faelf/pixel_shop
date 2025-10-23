from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactMessageForm
from .models import ContactMessage


def home(request):
    """
    Renders the home page, exteded from base.html.
    """
    return render(request, "home/home.html")


def contact_page(request):
    """
    Renders the contact page and handles contact form submissions.
    The messages will be displayed for staff oldest first.
    """
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("home")
    else:
        form = ContactMessageForm()

    user_messages = ContactMessage.objects.all().order_by("created_at")
    context = {"form": form, "user_messages": user_messages}

    return render(request, "home/contact.html", context)


def is_staff_user(user):
    """
    Checks if the user is a staff member.
    """
    return user.is_staff


@login_required
@user_passes_test(is_staff_user)
def delete_message(request, message_id):
    """
    Handles the deletion of a single message.
    Only accessible to staff users.
    Redirects back to the contact page after deletion.
    """

    if request.method == "POST":
        message = get_object_or_404(ContactMessage, pk=message_id)
        message.delete()
        messages.success(request, f"Message from {message.name} successfully deleted.")
        return redirect("contact")
    return redirect("contact")
