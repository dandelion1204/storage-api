from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models

class ModelTests(TestCase):

    def test_create_user_with_email(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_normalizes(self):
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com'],
        ]

        for email,expected in sample_emails:
            user = get_user_model().objects.create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
                email='test1@example.com',
                password='test123',
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_product(self):
        product = models.Product.objects.create(
            title= 'Apple Watch',
            item_num='P0001',
            quantity= Decimal('100'),
            description = 'A fancy watch'
        )

        self.assertEqual(str(product), product.title)

    def test_create_ingredient(self):
        ingredient = models.Ingredient.objects.create(
                name = 'plastic ball',
                item_num = 'I0001',
                quantity = Decimal('100'),
                lot = '24111401',
                supplier = 'Orange Inc.',
        )

        self.assertEqual(str(ingredient), ingredient.name)


