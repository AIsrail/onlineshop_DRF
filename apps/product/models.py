from django.conf import settings
from django.db import models

from apps.category.models import Category
from apps.product.utils import upload_image_path


class DateABC(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(DateABC):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=False)
    quantity = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products',
                                 null=True)

    def __str__(self):
        return f"{self.title} --> {self.price}"


class ProductImage(DateABC):
    image = models.ImageField(upload_to=upload_image_path)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )

    @property
    def get_absolute_image_url(self):
        return f'{self.image.url}'

    def __str__(self):
        return f'{self.product.title}.jpg'









