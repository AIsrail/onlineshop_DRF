from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.product.models import Product, ProductImage


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, ]
    list_display = ('id', 'title', 'price', 'discount', 'get_image')

    def get_image(self, obj):
        img = obj.images.first()
        if img:
            return mark_safe(f'<img src="{img.get_absolute_image_url}" width="50" height="50">')
        else:
            return ""


admin.site.register(Product, ProductAdmin)


