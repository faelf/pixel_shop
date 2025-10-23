from django.urls import path
from .views import view_trolley, add_to_trolley

urlpatterns = [
    path("", view_trolley, name="trolley"),
    path("add/<item_id>", add_to_trolley, name="add_to_trolley"),
]
