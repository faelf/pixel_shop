from django.urls import path
from .views import home, contact_page

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact_page, name="contact"),
]
