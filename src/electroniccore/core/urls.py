from django.urls import path
from core.views import (DeleteItemView, DetailCategoryView, HomeView, AccountView, ShopView, ProductView,
                        CheckoutView, PaymentView, Login, Logout, SignupView, CartView, SearchView, 
                        SortProductView, FilterProductView, CreateCartView, ListCartView,
                        DeleteCartView,

                        )


app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('my-account/', AccountView.as_view(), name='account'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<str:product_slug>', ProductView.as_view(), name='product'),
    path('checkout/<int:order_id>', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('categories/<str:category_slug>',
         DetailCategoryView.as_view(), name='show_category'),
    path('articles/search', SearchView.as_view(), name='search'),
    path('articles/filter/<str:sort_type>',
         FilterProductView.as_view(), name='filter'),
    path('articles/sort/<str:sort_type>',
         SortProductView.as_view(), name='sort'),
    # Cart urls
    path('cart/', CartView.as_view(), name='cart'),
    path('my-cart/', ListCartView.as_view(), name='list_cart'),

    path('cart/add/<str:product_slug>', CreateCartView.as_view(), name='add_cart'),
    path('delete-item/<str:product_slug>', DeleteItemView.as_view(), name='delete_item'),
    path('delete-cart/<int:order_id>', DeleteCartView.as_view(), name='delete_order'),
    #path('update-cart/<int:qte>', UpdateCartView.as_view(), name='delete_order'),


]
