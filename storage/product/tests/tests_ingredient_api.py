from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Product, Ingredient
from product.serializers import IngredientSerializer #IngredientDetailSerializer

INGREDIENT_URL = reverse('product:ingredient-list')

def detail_url(ingredient_id):
    return reverse('product:ingredient-detail', args=[ingredient_id])

def create_ingredient(**params):
    defaults = {
        'name': 'Plastic ball',
        'item_num': 'I0001',
        'quantity': Decimal('100'),
        'lot': 'S1403001',
        'supplier': 'Orange Inc.'
    }
    defaults.update(**params)

    ingredient = Ingredient.objects.create(**defaults)
    return ingredient


class PublicIngredientAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email= 'test@example.com',
            password= 'testpass123',
            name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_lists(self):
        create_ingredient(item_num='I0001')
        create_ingredient(item_num='I0002')

        res = self.client.get(INGREDIENT_URL)

        ingredient = Ingredient.objects.all().order_by('-item_num')
        serializer = IngredientSerializer(ingredient, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_ingredient_partial(self):
         ori_name = 'perl'
         ingredient = create_ingredient(item_num='I0001', name=ori_name)
         payload = {'item_num':'I0010'}

         url = detail_url(ingredient.id)
         res = self.client.patch(url, payload)

         ingredient.refresh_from_db()
         self.assertEqual(res.status_code, status.HTTP_200_OK)
         self.assertEqual(ingredient.item_num, payload['item_num'])
         self.assertEqual(ingredient.name, ori_name)

    def test_delete_ingredient(self):
        ingredient = create_ingredient(item_num='I0001', name='perl')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id).exists())



