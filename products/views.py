from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product


# Create your views here.
def products_list(request):
    products = Product.objects.all()

    category_name = request.GET.getlist("category")
    if category_name:
        products = products.filter(categories__name__in=category_name)

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "category_name": category_name,
    }

    if request.htmx:
        return render(request, "products/product_card.html", context)

    return render(request, "products/products_list.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/product_detail.html", {"product": product})
