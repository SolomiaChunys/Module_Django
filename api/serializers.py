from rest_framework import serializers
from shop.models import User, Product, Order, Return


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
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


# class OrderSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     product = ProductSerializer()
#
#     class Meta:
#         model = Order
#         fields = [
#             'id',
#             'user',
#             'product',
#             'count'
#         ]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'product',
            'count'
        ]

    def create(self, validated_data):
        user = validated_data.pop('user')
        product = validated_data.pop('product')

        get_user, created = User.objects.get_or_create(**user)
        get_product, created = Product.objects.get_or_create(**product)

        create_order = Order.objects.create(user=get_user, product=get_product, **validated_data)
        return create_order


class ReturnSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Return
        fields = [
            'id',
            'order',
        ]

    def create(self, validated_data):
        order = validated_data.pop('order')

        get_order, created = Order.objects.get_or_create(**order)

        create_return = Return.objects.create(order=get_order, **validated_data)
        return create_return


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
