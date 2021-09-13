from django.urls import path
from core.views import (HomeView, AccountView, ShopView, ProductView,
                        CheckoutView, PaymentView, Login,
                        Logout, SigninView,
                        )


app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my-account/', AccountView.as_view(), name='account'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<str:product_slug>', ProductView.as_view(), name='product'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signin/', SigninView.as_view(), name='signin'),

]
