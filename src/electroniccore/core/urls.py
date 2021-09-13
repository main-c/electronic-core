from django.contrib import admin
from django.urls import path
from core.views import (HomeView, AccountView, ShopView, ProductView,
    CartView, CheckoutView, PaymentView, LoginView, LogoutView, SignupView,
    )  

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my-account/', AccountView.as_view(), name='account'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
