from rest_framework import viewsets, authentication, permissions, mixins
from rest_framework.authtoken.views import ObtainAuthToken
#from rest_framework.settings import api_settings
from product.serializers import (
                        ProductSerializer,
                        ProductDetailSerializer,
                        IngredientSerializer,
                        IngredientDetailSerializer
                        )
from core.models import Product, Ingredient


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
    serializer_class = IngredientSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        return self.queryset.all().order_by('-item_num')


