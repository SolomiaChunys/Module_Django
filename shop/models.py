from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    wallet = models.DecimalField(decimal_places=2, default=10000, max_digits=12)

    def __str__(self):
        return f"{self.username}"


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    count = models.PositiveIntegerField()
    data_creation = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_creation']

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    datatime_of_purchase = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datatime_of_purchase']

    def __str__(self):
        return f"{self.user}: {self.product.name}"


class Return(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='returns')
    datatime_of_return = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['datatime_of_return']

    def __str__(self):
        return f"{self.order.user.username}: {self.order.product.name} {self.order.product.count}"