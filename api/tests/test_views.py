from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from shop.models import Product
from django.urls import reverse
from api.factory import ProductFactory

User = get_user_model()


class ProductTest(APITestCase):
    def setUp(self):
        self.product = ProductFactory()

    def test_create(self):
        data = {
            'name': 'New product',
            'description': 'Short description for product',
            'price': 40.0,
            'count': 10,
        }
        url = reverse('product-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_retrieve(self):
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        new_data = {
            'name': 'Updated product',
            'description': 'New description for product',
            'price': 30.0,
            'count': 20,
        }
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.put(url, new_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Product.objects.get(id=self.product.id).name, new_data['name'])

    def test_delete(self):
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
