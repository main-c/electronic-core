from django.urls import path
from core.views import (DetailCategoryView, HomeView, AccountView, ShopView, ProductView,
                        CheckoutView, PaymentView, Login,
                        Logout, SignupView, CartView, SearchView, SortProductView, FilterProductView,
                        CheckoutverView, CommandView, CommandView, DashboardView, BillingaddressView,
                        DetailaccountView
                        )
CheckoutverView

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my-account/', AccountView.as_view(), name='account'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<str:product_slug>', ProductView.as_view(), name='product'),
    path('checkout/<int:order_id>', CheckoutView.as_view(), name='checkouts'),
    path('checkout/', CheckoutverView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('cart/', CartView.as_view(), name='cart'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('categories/<str:category_slug>', DetailCategoryView.as_view(), name='show_category'),
    path('articles/search', SearchView.as_view(), name='search'),
    path('articles/filter/<str:sort_type>', FilterProductView.as_view(), name='filter'),
    path('articles/sort/<str:sort_type>', SortProductView.as_view(), name='sort'),
    path('command/', CommandView.as_view(), name='command'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('billing_address/', BillingaddressView.as_view(), name='billing_address'),
    path('detail_account/', DetailaccountView.as_view(), name='detail_account'),
]
