from api.serializers import (
    UserSerializer,
    ProductSerializer,
    OrderSerializer,
    ReturnSerializer,
)
from rest_framework.exceptions import ValidationError
from rest_framework import permissions, viewsets
from shop.models import User, Product, Order, Return
from rest_framework.decorators import action
from api.filters import IsOwnerOfOrder
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token


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
