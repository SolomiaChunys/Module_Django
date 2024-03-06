from rest_framework import serializers
from shop.models import User, Product, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'wallet'
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'count'
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'product',
            'count'
        ]


class NewOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'product',
            'count'
        ]

    def create(self, validated_data):
        user = validated_data.get('user')
        get_user = User.objects.get_or_create(**user)
        create_order = Order.objects.create(user=get_user, **validated_data)
        return create_order


class UserOrderSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'wallet',
            'orders'
        ]

    def create(self, validated_data):
        orders = validated_data.get('orders')
        create_user = User.objects.create(**validated_data)

        for order in orders:
            create_order = Order.objects.create(user=create_user, **order)

        return create_user
