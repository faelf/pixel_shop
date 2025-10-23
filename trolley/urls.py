from django.urls import path
from .views import (
    view_trolley,
    add_to_trolley,
    update_trolley,
    delete_item_from_trolley,
)

urlpatterns = [
    path("", view_trolley, name="trolley"),
    path("add/<int:item_id>/", add_to_trolley, name="add_to_trolley"),
    path("update/<int:item_id>/", update_trolley, name="update_trolley"),
    path("remove/<int:item_id>/", delete_item_from_trolley, name="remove_from_trolley"),
]
