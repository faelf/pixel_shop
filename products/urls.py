from django.urls import path
from . import views

urlpatterns = [
    path("", views.products_list, name="products_list"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
]
