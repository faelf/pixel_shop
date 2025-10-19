from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.friendly_name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    categories = models.ManyToManyField(Category, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.name
