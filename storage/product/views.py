from rest_framework import (
                                viewsets,
                                authentication,
                                permissions,
                                mixins,
                                status
                            )
from rest_framework.decorators import action
from rest_framework.response import Response
from product.serializers import (
                        ProductSerializer,
                        ProductDetailSerializer,
                        IngredientSerializer,
                        IngredientDetailSerializer,
                        IngredientLotSerializer
                        )
from core.models import (
                            Product,
                            Ingredient,
                            ProductIngredients,
                            IngredientLot
                        )
from django.shortcuts import render
from decimal import Decimal
from django.db.models import Sum

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

def add_ingredient(request):
    return render(request, 'ingredients/add_ingredient.html')

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
    #queryset = Ingredient.objects.none()

    def get_queryset(self):
        return self.queryset.all().order_by('-item_num')
        #return self.queryset.annotate(total_quantity=Sum('lots__quantity')).order_by('-item_num')


    def get_serializer_class(self):
        if self.action == 'list':
            return IngredientSerializer

        return self.serializer_class

    @action(detail=True, methods=['post'], url_path='add-lot')
    def add_lot(self, request, pk=None):
        ingredient = self.get_object()
        serializer = IngredientLotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ingredient=ingredient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientLotViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientLotSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = IngredientLot.objects.all()

    @action(detail=True, methods=['patch'], url_path='update_quantity')
    def update_quantity(self, request, pk=None):
        lot = self.get_object()

        change = request.data.get('quantity')
        if change is None:
            return Response({"error": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            change = int(change)
        except ValueError:
            return Response({"error": "Quantity must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        # 檢查最終結果不能是負數
        if lot.quantity + change < 0:
            return Response({"error": "Quantity cannot be negative"}, status=status.HTTP_400_BAD_REQUEST)

        lot.quantity += change
        lot.save()
        serializer = self.get_serializer(lot)
        return Response(serializer.data)

