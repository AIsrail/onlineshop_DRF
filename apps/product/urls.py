from django.urls import path, include

from apps.product import views
from apps.product.views import *

app_name = 'product'

urlpatterns = [
    path('', views.ListProductView.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product-api/', include('apps.product.api.urls')),
    path('product-delete/', ProductRetrieveDestroy.as_view()),
]


