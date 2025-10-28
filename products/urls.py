from django.urls import path
from . import views

urlpatterns = [
    path("", views.products_list, name="products_list"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
    path("product/<int:product_id>/edit/", views.product_edit, name="product_edit"),
    path("product/add/", views.product_add, name="product_add"),
    path(
        "product/<int:product_id>/delete/", views.product_delete, name="product_delete"
    ),
]
