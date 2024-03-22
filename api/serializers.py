from rest_framework import serializers
from shop.models import User, Product, Order, Return
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import password_validation


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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'auth_token',
        )
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        )

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
