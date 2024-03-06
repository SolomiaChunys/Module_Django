from api.serializers import UserSerializer, ProductSerializer, OrderSerializer, NewOrderSerializer, UserOrderSerializer
from shop.models import User, Product, Order

# 2.1
user_data = {
    'username': 'lisa',
    'email': 'lisa@gmail.com',
    'password': 'Lissa11_',
}

user_serializer = UserSerializer(data=user_data)
if user_serializer.is_valid():
    user_obj = user_serializer.save()
else:
    print(user_serializer.errors)

product_data = {
    'name': 'Car toy',
    'description': 'Toy for kids 3+',
    'price': 400.00,
    'count': 20,
}

product_serializer = ProductSerializer(data=product_data)
if product_serializer.is_valid():
    product_obj = product_serializer.save()
else:
    print(product_serializer.errors)

order_data = {
    'user': user_obj.id,
    'product': product_obj.id,
    'count': 5,
}

order_serializer = OrderSerializer(data=order_data)
if order_serializer.is_valid():
    order = order_serializer.save()
else:
    print(order_serializer.errors)

# 2.2
user = User.objects.last()
product = Product.objects.first()
last_order = Order.objects.first()

user_serializer = UserSerializer(user)
product_serializer = ProductSerializer(product)
order_serializer = OrderSerializer(last_order)

# user_serializer.data
# product_serializer.data
# order_serializer.data
#
#
# >>> user_serializer.data
# {'id': 6, 'username': 'lisa', 'password': 'Lissa11_', 'wallet': '10000.00'}
#
# >>> product_serializer.data
# {'id': 16, 'name': 'Car toy', 'description': 'Toy for kids 3+', 'price': '400.00', 'count': 20}
#
# >>> order_serializer.data
# {'id': 31, 'user': 6, 'product': 16, 'count': 5}

# 3.1
new_order = Order.objects.first()
neworder_serializer = NewOrderSerializer(new_order)
# neworder_serializer.data
#
# >>> neworder_serializer.data
# {'id': 31, 'user': OrderedDict([('id', 6), ('username', 'lisa'), ('password', 'Lissa11_'), ('wallet', '10000.00')]), 'product':
#  16, 'count': 5}

# 4.1
user_orders = User.objects.last()
user_orders_serializer = UserOrderSerializer(user_orders)
user_orders_serializer.data

>>> user_orders_serializer.data
{'id': 6, 'username': 'lisa', 'password': 'Lissa11_', 'wallet': '10000.00', 'orders': [OrderedDict([('id', 31),
('user', 6), ('product', 16), ('count', 5)]), OrderedDict([('id', 30), ('user', 6), ('product', 15), ('count', 5)])]}
