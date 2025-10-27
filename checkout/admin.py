from django.contrib import admin
from .models import Order, OrderLineItem
# Register your models here.


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ("lineitem_total",)

    readonly_fields = ("product", "quantity", "lineitem_total")


class OderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        "order_number",
        "date",
        "delivery_cost",
        "order_total",
        "grand_total",
    )

    fields = (
        "order_number",
        "date",
        "full_name",
        "email",
        "phone_number",
        "street_address1",
        "street_address2",
        "postcode",
        "town_or_city",
        "county",
        "country",
        "delivery_cost",
        "order_total",
        "grand_total",
    )

    list_display = (
        "order_number",
        "date",
        "full_name",
        "email",
    )

    ordering = ("-date",)


admin.site.register(Order, OderAdmin)
