from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View


class HomeView(TemplateView):
	template_name = "core/home.html"


class AccountView(TemplateView): #Dashboard
	template_name = "core/account.html"


class ShopView(TemplateView):
	template_name = "core/shop.html"


class ProductView(TemplateView):
	template_name = "core/product.html"


class CartView(TemplateView): #Panier
	template_name = "core/cart.html"

class CheckoutView(TemplateView): #Formulaire validation commande
	template_name = "core/checkout.html"


class PaymentView(TemplateView):
	template_name = "core/payment.html"


class LoginView(TemplateView):
	template_name = "core/login.html"


class LogoutView(TemplateView):
	template_name = "core/logout.html"


class SignupView(TemplateView):
	template_name = "core/signup.html"

