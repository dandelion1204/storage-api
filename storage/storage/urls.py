"""storage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path,include
from core import views as core_views
from user import views as user_view
from product import views as product_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/user/', include('user.urls')),
    path('api/product/', include('product.urls')),
    path('', core_views.home, name='home'),
    path('login/', user_view.login_page, name='login'),
    path('register/', user_view.register_page, name='register'),
    path('products/', product_view.product_list, name='product_list'),
    path('products/add_product', product_view.add_product, name='add_product'),
    path('products/add_ingredient', product_view.add_ingredient, name='add_ingredient'),
    path('products/<int:pk>/', product_view.product_detail, name='product_detail'),
    path('ingredients/', product_view.ingredient_list, name='ingredient_list'),
    path('ingredients/<int:pk>/', product_view.ingredient_detail, name='ingredient_detail'),
    path('products/<int:pk>/adjust-ingredient/', product_view.product_ingredient_adjust, name='adjust_ingredient'),
]
