from django.test import TestCase
from shop.views import LoginPage, LogoutPage, SignupPage
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Lisa',
            password='lisa_1234'
        )

    def test_login(self):
        url = reverse('login_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'Lisa',
            'password': 'lisa_1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, reverse('home'))

    def test_logout(self):
        self.client.login(
            username='Lisa',
            password='lisa_1234'
        )

        url = reverse('logout_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, reverse('home'))

    def test_signup(self):
        url = reverse('signup_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'Johny',
            'email': 'johny@gmail.com',
            'password1': 'johny_1234',
            'password2': 'johny_1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, reverse('home'))

        user = User.objects.get(username='Johny')
        self.assertIsNotNone(user)
