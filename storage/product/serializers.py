from rest_framework import serializers
from core.models import Product, Ingredient, ProductIngredients, IngredientLot
from django.db import transaction
from decimal import Decimal
from django.db.models import Sum

class IngredientSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'item_num', 'total_quantity']
        read_only_fields = ['id']

    def get_total_quantity(self, obj):
        return obj.lots.aggregate(total=Sum('quantity'))['total'] or 0


class IngredientLotSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientLot
        fields = ['id', 'lot', 'quantity', 'supplier']
        read_only_fields = ['id']


class IngredientDetailSerializer(serializers.ModelSerializer):
    lots = IngredientLotSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()

    class Meta(IngredientSerializer.Meta):
        fields = IngredientSerializer.Meta.fields + ['lots']
        read_only_fields = ['id']

    def get_total_quantity(self, obj):
        return obj.lots.aggregate(total=Sum('quantity'))['total'] or 0



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','title','item_num']
        read_only_fields = ['id']


class ProductIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = ProductIngredients
        fields = ['id', 'product', 'ingredient', 'ingredient_name', 'quantity']

    def create(self, validated_data):
        # 如果是單筆就走預設的
        return super().create(validated_data)

class ProductDetailSerializer(ProductSerializer):
    ingredients = ProductIngredientSerializer(many=True, read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description', 'ingredients']
        read_only_fields = ['id']







