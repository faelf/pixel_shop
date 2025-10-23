from django.urls import path
from .views import home, contact_page, delete_message

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact_page, name="contact"),
    path("contact/delete/<int:message_id>/", delete_message, name="delete_message"),
]
