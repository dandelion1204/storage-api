from rest_framework import viewsets, authentication, permissions, mixins
from product.serializers import (
                        ProductSerializer,
                        ProductDetailSerializer,
                        IngredientSerializer,
                        IngredientDetailSerializer
                        )
from core.models import Product, Ingredient, ProductIngredients
from django.shortcuts import render
from decimal import Decimal

def product_list(request):
    return render(request, 'products/product_list.html')

def product_detail(request, pk):
    return render(request, 'products/product_detail.html', {'product_id': pk})

def ingredient_list(request):
    return render(request, 'ingredients/ingredient_list.html')

def ingredient_detail(request, pk):
    return render(request, 'ingredients/ingredient_detail.html', {'ingredient_id': pk})

def add_product(request):
    return render(request, 'products/add_product.html')

def product_ingredient_adjust(request, pk):
    return render(request, 'products/adjust_ingredient.html', {'product_id': pk})

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer

        return self.serializer_class


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('-item_num')

    def get_serializer_class(self):
        if self.action == 'list':
            return IngredientSerializer

        return self.serializer_class


