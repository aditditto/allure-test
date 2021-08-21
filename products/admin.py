from django.contrib import admin
from .models import Product, Review

# Register your models here.

admin.site.register(Review)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'is_published', 'last_updated')
