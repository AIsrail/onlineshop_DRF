from django.urls import path

from apps.main_app import views
from apps.user.views import *
from apps.order.views import *
app_name = 'main_app'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),

    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('products/', views.ProductView.as_view(), name='products-list'),
    path('products/<int:pk>/', views.ProductDetailedView.as_view(), name='product-detail'),
    path('products-update/<int:pk>/', views.ProductUpdateView.as_view()),
    path('products-delete/<int:pk>/', views.ProductDeleteView.as_view()),

    path('register/', RegistrationAPIView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('orders/', OrderViewSet.as_view),

]