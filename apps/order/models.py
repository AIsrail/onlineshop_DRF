from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import DateABC, Product

User = get_user_model()


class Order(DateABC):
    ORDER_STATUS = (
        ('Paid', 'paid'),
        ('Not Paid', 'not paid')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    discount = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(choices=ORDER_STATUS, max_length=30, default='not paid')
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.status} {self.user}'


class OrderProduct(DateABC):
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_products', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.product.price * self.quantity

