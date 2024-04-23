from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'display_product_image']

    def display_product_image(self, obj):
        return obj.product_image.url if obj.product_image else None

    display_product_image.short_description = 'Product Image'
