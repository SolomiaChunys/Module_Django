from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from api.factory import UserFactory

User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_login(self):
        url = reverse('auth-login')
        data = {
            'username': 'Rose',
            'password': 'rose1234_',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register(self):
        url = reverse('auth-register')
        data = {
            'username': 'Jenny',
            'email': 'jenny@gmail.com',
            'password': 'jenny1234_',
            'first_name': 'Jenny',
            'last_name': 'Grey',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logout(self):
        url = reverse('auth-logout')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
