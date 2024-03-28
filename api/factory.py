from shop.models import Product
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = 'Rose'
    email = 'rose@gmail.com'
    password = 'rose1234_'


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = 'My test product'
    description = 'The description of product'
    price = 50.0
    count = 5