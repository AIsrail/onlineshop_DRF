"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ecommerce import settings
from apps.main_app.views import *

router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main_app.urls')),
    path('products/', include('apps.product.urls')),
    path('api/v1/accounts/', include('apps.user.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/categories/', CategoryListView.as_view()),
    path('api/v1/add-image/', ProductImageView.as_view()),

    path('api/v1/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
