from rest_framework import serializers
from core.models import Product, Ingredient, ProductIngredients, IngredientLot
from django.db import transaction
from decimal import Decimal
from django.db.models import Sum


class ProductIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = ProductIngredients
        fields = ['id', 'product', 'ingredient', 'ingredient_name', 'quantity', 'unit']

    def update(self, instance, validated_data):
        ingredients_data = validated_data.get('ingredients', [])
        for ingredient_data in ingredients_data:
            if Decimal(ingredient_data.get('quantity', 0)) == 0:
                ProductIngredients.objects.filter(
                    product=instance,
                    ingredient_id=ingredient_data['ingredient']
                ).delete()

        return instance



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','title','item_num']
        extra_kwargs = {
            'title': {'required': False},
            'item_num': {'required': False}
        }
        read_only_fields = ['id']


class ProductDetailSerializer(ProductSerializer):
    ingredients = ProductIngredientSerializer(source='productingredients_set', many=True, required=False)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description', 'ingredients']


    def create(self, validated_data):
        ingredients_data = validated_data.pop('productingredients_set', [])

        with transaction.atomic():
            product = super().create(validated_data)

            # 創建嵌套的 ingredients
            for ingredient_data in ingredients_data:
                ProductIngredients.objects.create(product=product, **ingredient_data)

            return product

    def update(self, instance, validated_data):
        request_data = self.context['request'].data

        # 根據數據類型決定如何獲取 ingredients
        if hasattr(request_data, 'getlist'):  # 測試用例的情況
            ingredients_raw = request_data.getlist('ingredients', [])
            # 需要解析字符串
            ingredients_data = []
            for ingredient_str in ingredients_raw:
                try:
                    import ast
                    ingredient_data = ast.literal_eval(ingredient_str)
                    ingredients_data.append(ingredient_data)
                except Exception as e:
                    print(f"Error parsing ingredient: {e}")
                    continue
        else:  # 前端 AJAX 的情況
            ingredients_data = request_data.get('ingredients', [])

        # 更新 Product 基本資料
        for attr, value in validated_data.items():
            if attr != 'productingredients_set':
                setattr(instance, attr, value)
        instance.save()

        # 處理 ingredients
        if ingredients_data:
            # 刪除現有的關聯
            instance.productingredients_set.all().delete()

            # 建立新的關聯
            for ingredient_data in ingredients_data:
                try:
                    quantity = str(ingredient_data.get('quantity', '0'))
                    quantity_decimal = Decimal(quantity)

                    if quantity_decimal > 0:
                        ProductIngredients.objects.create(
                            product=instance,
                            ingredient_id=ingredient_data['ingredient'],
                            quantity=quantity_decimal,
                            unit=ingredient_data.get('unit', '')
                        )

                except Exception as e:
                    print(f"Error processing ingredient: {e}")
                    print(f"ingredient_data: {ingredient_data}")
                    continue

        return instance

class IngredientSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'item_num', 'total_quantity']
        #fields = ['id', 'name', 'item_num']
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




