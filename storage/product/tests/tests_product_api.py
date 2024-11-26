from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Product, Ingredient, ProductIngredients
from product.serializers import (
            ProductSerializer,
            ProductDetailSerializer,
            ProductIngredientSerializer,
            )


PRODUCT_URL = reverse('product:product-list')

def detail_url(product_id):
    return reverse('product:product-detail', args=[product_id])

def create_product(**params):
    defaults = {
        'title': 'Apple Watch',
        'item_num': 'P0001',
        'quantity': Decimal('200'),
        'description': 'A fancy watch',
    }
    defaults.update(**params)

    product = Product.objects.create(**defaults)
    return product


class PublicProductAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email= 'test@example.com',
            password= 'testpass123',
            name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_product_lists(self):
        create_product(item_num='P0001')
        create_product(item_num='p0002')

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_product_detail(self):
        product = create_product(item_num='P0001')

        url = detail_url(product.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)

    def test_create_product(self):
        payload = {
            'title':'Apple Watch',
            'item_num':'P0001',

        }

        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        for i,j in payload.items():
            self.assertEqual(getattr(product,i), j)

    def test_partial_update(self):
        ori_item_num = 'P0001'
        product = create_product(
            title='Apple Watch',
            item_num=ori_item_num,
        )

        payload = {
            'title':'Apple pencil',
        }
        url = detail_url(product.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.title, payload['title'])
        self.assertEqual(product.item_num, ori_item_num)

    def test_ful_update(self):
        product = create_product(
            title='Apple Watch',
            item_num='P0001',
            quantity=Decimal(10),
            description='A fancy watch',
        )

        payload = {
            'title':'Apple Watch',
            'item_num':'P0001',
            'quantity':Decimal(10),
            'description':'A fancy watch',
        }
        url = detail_url(product.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        for i,j in payload.items():
            self.assertEqual(getattr(product,i),j)

    def test_delete_product(self):
        product = create_product(
            title='Apple Watch',
            item_num='P001',
        )

        url = detail_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())

    def test_create_duplicate_item_num_error(self):
        create_product(
            title='Apple Watch',
            item_num='P001',
        )
        payload = {
            'title':'Apple pencil',
            'item_num':'P001',
        }

        res = self.client.post(PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dproduct_ingredient_qiantity(self):
        product = create_product(
            title='Apple Watch',
            item_num='P001',
        )

        product2 = create_product(
            title='Apple Pencil',
            item_num='P002',
        )

        ingredient1 = Ingredient.objects.create(
            name = 'A',
            item_num = 'I0001',
            quantity = Decimal('100')
        )
        ingredient2 = Ingredient.objects.create(
            name = 'B',
            item_num = 'I0002',
            quantity = Decimal('100')
        )
        ingredient3 = Ingredient.objects.create(
            name = 'C',
            item_num = 'I0003',
            quantity = Decimal('100')
        )

        ProductIngredients.objects.create(
            product = product,
            ingredient = ingredient1,
            quantity = Decimal('100')
        )

        ProductIngredients.objects.create(
            product = product,
            ingredient = ingredient2,
            quantity = Decimal('200')
        )

        ProductIngredients.objects.create(
            product = product,
            ingredient = ingredient3,
            quantity = Decimal('300')
        )

        ProductIngredients.objects.create(
            product = product2,
            ingredient = ingredient1,
            quantity = Decimal('400')
        )

        url = detail_url(product.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)
        for ingredient in res.data['ingredients']:
            self.assertNotEqual(ingredient['product'], product2.id)


