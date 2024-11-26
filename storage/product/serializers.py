from rest_framework import serializers
from core.models import Product, Ingredient, ProductIngredients


class ProductIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = ProductIngredients
        fields = ['id', 'product', 'ingredient', 'ingredient_name', 'quantity', 'unit']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','title','item_num','quantity',]
        read_only_fields = ['id']


class ProductDetailSerializer(ProductSerializer):
    ingredients = ProductIngredientSerializer(source='productingredients_set', many=True, required=False)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description', 'ingredients']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'item_num', 'quantity']
        read_only_fields = ['id']


class IngredientDetailSerializer(IngredientSerializer):

    class Meta(IngredientSerializer.Meta):
        fields = IngredientSerializer.Meta.fields + ['lot', 'supplier']





