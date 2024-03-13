from django.urls import path, include
from api.views import UserViewSet, ProductViewSet, OrderViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'product', ProductViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
