from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .forms import ProductForm
from .models import Product


def products_list(request):
    """
    A view to show all products, including sorting and search queries
    """
    products = Product.objects.all().order_by("name")

    search_query = request.GET.get("q", "")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    category_name = request.GET.getlist("category")
    if category_name:
        products = (
            products.filter(categories__name__in=category_name)
            .annotate(
                matching_categories=Count(
                    "categories", filter=Q(categories__name__in=category_name)
                )
            )
            .filter(matching_categories=len(category_name))
            .distinct()
        )

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "category_name": category_name,
        "search_query": search_query,
    }

    if request.htmx:
        return render(request, "products/product_card.html", context)

    return render(request, "products/products_list.html", context)


def product_detail(request, product_id):
    """
    A view to show individual product details
    """
    product = get_object_or_404(Product, pk=product_id)
    return render(
        request, "products/product_detail.html", {"product": product}
    )


@login_required
def product_edit(request, product_id):
    """
    A view to edit a product
    """
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if request.POST.get("remove_image"):
            if product.image:
                product.image.delete(save=False)
                product.image = None

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_detail", product_id=product_id)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/product_edit.html",
        {"form": form, "product": product},
    )


@login_required
def product_add(request):
    """
    A view to add a product
    """
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product added successfully!")
            return redirect("product_detail", product_id=product.id)
    else:
        form = ProductForm()

    return render(request, "products/product_add.html", {"form": form})


@login_required
def product_delete(request, product_id):
    """
    A view to delete a product
    """
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product_name = product.name
        product.delete()
        messages.success(
            request, f'Product "{product_name}" deleted successfully!'
        )
        return redirect("products_list")

    return redirect("product_detail", product_id=product_id)
