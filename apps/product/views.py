from django.views.generic import ListView, DetailView
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from .api.paginations import *
from apps.product.models import *
from .models import *
from .api.serializers import *


class ListProductView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(in_stock=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAPISerializer
    pagination_class = CustomOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class ProductRetrieveDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = Product.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Нельзя изменить этот продукт, не созданный вами')


    def patch(self, request, *args, **kwargs):
        post = Product.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.partial_update(request, *args, **kwargs)
        else:
            raise ValidationError('Ты не можешь вносить изменения в чужой пост, дядя')

    def put(self, request, *args, **kwargs):
        post = Product.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.partial_update(request, *args, **kwargs)
        else:
            raise ValidationError('Нельзя обновить полностью то, что не создано вами')