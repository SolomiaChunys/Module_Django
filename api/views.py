from api.serializers import (
    UserSerializer,
    ProductSerializer,
    OrderSerializer,
    ReturnSerializer,
    EmptySerializer,
    UserLoginSerializer,
    AuthUserSerializer,
)
from api.filters import IsOwnerOfOrder
from shop.models import Product, Order, Return
from rest_framework.exceptions import ValidationError
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model, logout
from . import serializers
from .utils import get_and_authenticate_user, create_user_account

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        amount = self.request.query_params.get('amount')

        if amount is not None:
            try:
                amount = float(amount)
                queryset = queryset.filter(wallet__gte=amount)
            except ValueError:
                return ValidationError('The parameter "amount" is not number')
        return queryset

    @action(detail=True, methods=['get'])
    def get_order_for_user(self, request, pk=None):
        user = self.get_object()
        orders = user.orders.all().values_list('id', flat=True)

        data = {
            'id': user.id,
            'username': user.username,
            'wallet': user.wallet,
            'orders': list(orders),
        }
        return Response(data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_name = self.request.query_params.get('filter_name')

        if filter_name is not None:
            queryset = queryset.filter(name__icontains=filter_name)

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [IsOwnerOfOrder]


class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all().order_by('datatime_of_return')
    serializer_class = ReturnSerializer


# Отримання токену
class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            if not created:
                if datetime.now() - token.created > timedelta(minutes=10):
                    token.delete()
                    token = Token.objects.create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.pk,
            })
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

