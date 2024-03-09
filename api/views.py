from api.serializers import UserSerializer, ProductSerializer, OrderSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import permissions, viewsets
from shop.models import User, Product, Order
from rest_framework.decorators import action
from rest_framework.response import Response


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

    def perform_create(self, serializer):
        product_data = serializer.save()
        product_data.name += '!'
        product_data.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_name = self.request.query_params.get('filter_name')

        if filter_name is not None:
            queryset = queryset.filter(name__icontains=filter_name)

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
