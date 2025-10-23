from django.urls import path
from .views import view_trolley

urlpatterns = [
    path("", view_trolley, name="trolley"),
]
