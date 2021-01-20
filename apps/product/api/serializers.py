from rest_framework import serializers

from apps.category.serializers import CategorySerializer
from apps.product.models import Product, ProductImage

from rest_framework import serializers
from .models import *


class ProductAPIImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductAPISerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    images = ProductAPIImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'images', 'category', 'id', 'title', 'description'
        )


