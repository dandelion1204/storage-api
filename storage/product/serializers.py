from rest_framework import serializers
from core.models import Product, Ingredient


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','title','item_num','quantity']
        read_only_fields = ['id']


class ProductDetailSerializer(ProductSerializer):

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'item_num', 'quantity']
        read_only_fields = ['id']


class IngredientDetailSerializer(IngredientSerializer):

    class Meta(IngredientSerializer):
        fields = IngredientSerializer.Meta.fields + ['lot', 'supplier']


