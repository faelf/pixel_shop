from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path("", views.checkout_view, name="checkout"),
    path("success/<order_number>", views.checkout_success, name="checkout_success"),
    path("order/<order_number>/", views.order_detail, name="order_detail"),
    path("wh/", webhook, name="webhook"),
    path("cache_checkout_data/", views.cache_checkout_data, name="cache_checkout_data"),
]
