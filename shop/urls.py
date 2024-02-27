from django.urls import path
from shop import views


urlpatterns = [
    path('login/', views.LoginPage.as_view(), name='login_page'),
    path('logout/', views.LogoutPage.as_view(), name='logout_page'),
    path('signup/', views.SignupPage.as_view(), name='signup_page'),
    path('create/product/', views.ProductCreatePage.as_view(), name='create_product'),
    path('update/product/<int:pk>/', views.ProductUpdatePage.as_view(), name='update_product'),
    path('purchase/<int:pk>/', views.ProductPurchase.as_view(), name='purchase'),
    path('user_purchase/', views.PurchasePage.as_view(), name='user_purchase'),
    path('return/', views.ReturnAdminPage.as_view(), name='return_product'),
    path('send/return/<int:pk>/', views.CreateReturnPage.as_view(), name='create_return'),
    path('accept/return/<int:pk>/', views.AcceptReturnAdmin.as_view(), name='accept_return'),
    path('refuse/return/<int:pk>/', views.RefuseReturnAdmin.as_view(), name='refuse_return'),
    path('', views.ProductPage.as_view(), name='home'),
]