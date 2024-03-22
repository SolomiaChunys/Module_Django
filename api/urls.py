from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from api.views import (
    UserViewSet,
    ProductViewSet,
    OrderViewSet,
    ReturnViewSet,
    ObtainExpiringAuthToken,
    AuthViewSet,
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'product', ProductViewSet, basename='product')
router.register(r'order', OrderViewSet)
router.register(r'return', ReturnViewSet)
router.register('api/auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    # path('api-token-auth/', views.obtain_auth_token),
    path('api-token-auth/', ObtainExpiringAuthToken.as_view())
]

