from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.product.models import Product


from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.decorators import action

from .models import *
from .api.serializers import *
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .api.paginations import *



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

    # @action(detail=False, methods=['get'])
    # def search(self, request, pk=None):
    #     print(request.query_params)
    #     q = request.query_params.get('q')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(Q(title__icontains=q))
    #     serializer = PostSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_query = self.request.query_params.get('search')
    #     if search_query:
    #         queryset = queryset.annotate(
    #             similarity = TrigramSimilarity('title', search_query),
    #         ).filter(similarity__gt=0.2).order_by('-similarity')
    #     return queryset

class PostRetrievDestroy(generics.RetrieveUpdateDestroyAPIView):
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