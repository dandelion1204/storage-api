from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
LOGIN_URL = reverse('user:manage-user')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test User',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_exists_email_error(self):
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test User',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            'email':'test@example.com',
            'password':'123',
            'name':'Test User',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertFalse(user)

    def test_create_token(self):
        user_details = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test User',
        }
        create_user(**user_details)

        payload = {
            'email' : user_details['email'],
            'password' : user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_wrong_password(self):
        user_details = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test User',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password' : 'badpassword',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        user_details = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test User',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password' : '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrived_user_unauthrized(self):
        res = self.client.get(LOGIN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticate_successful(self):
        res = self.client.get(LOGIN_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,
            {
                'name': self.user.name,
                'email': self.user.email,
            }
        )

    def test_post_not_allowed_in_login(self):
        res = self.client.post(LOGIN_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {
            'name': 'New Name',
            'password': 'NewPassword',
        }
        res = self.client.patch(LOGIN_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
