from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.main_app.permissions import *
from apps.product.api.serializers import *
from apps.product.models import *


class IndexPageView(TemplateView):
    template_name = 'main_app/index.html'


class MyPaginationClass(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        # print(data[1])
        for i in range(self.page_size):
            text = data[i]['text']
            data[i]['text'] = text[:15] + '....'
            # print(data[1]['text'])
        return super().get_paginated_response(data)


class CategoryListView(generics. ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductAPISerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPaginationClass

    def get_serializer_context(self):
        return {"request": self.request}

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsProductUser, ]
        else:
            permissions = [IsAuthenticated, ]
        return[permission() for permission in permissions]

    def get_queryset(self):                     # фиьлтрация по неделям, когда созданы посты (можно сделать по дням)
        queryset = super().get_queryset()
        weeks_count = int(self.request.query_params.get('days', 0))
        print(self.request.query_params)
        if weeks_count > 0:
            start_date = timezone.now() - timedelta(weeks=weeks_count)
            queryset = queryset.filter(created_at__gte=start_date)  # gte -> greater than or equal
        return queryset

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = ProductAPISerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        # print(request.query_params)
        q = request.query_params.get('q')    # request.query_params  ==> request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = ProductAPISerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductImageView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductAPIImageSerializer

    def get_serializer_context(self):
        return {"request": self.request}



class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAPISerializer

class ProductDetailedView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAPISerializer

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAPISerializer

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAPISerializer


