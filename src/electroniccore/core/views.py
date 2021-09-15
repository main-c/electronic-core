
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from core.forms import LoginForm, CustomerForm, AdressForm, CheckoutForm
from django.contrib.auth import authenticate, login, logout
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from core.models import (Product, ProductImage,
                         Category, Customer, OrderItem, Order, Address)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(TemplateView):
    template_name = "core/home.html"


class CartView(TemplateView):
    template_name = "core/cart.html"


class AccountView(TemplateView):  # Dashboard
    template_name = "core/account.html"


class FilterProductView(View):
    template_name = "core/sale.html"

    def get(self, request, sort_type):
        product_list = Product.objects.all()
        if sort_type == 'on-solde':
            product_list = Product.objects.filter(status="On Sale").all()
        elif sort_type == 'new':
            product_list = Product.objects.filter(status="New").all()
        elif sort_type == 'price' and request.POST['price']:
            products_list = Product.objects.filter(
                price=request.POST['price']).all()

        paginator = Paginator(product_list, 12)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
        context = {"products": products}
        return render(request, self.template_name, context)


class SortProductView(View):
    template_name = "core/sale.html"

    def get(self, request, sort_type):
        product_list = Product.objects.all()
        if sort_type == 'plus-recents':
            product_list = Product.objects.order_by('-post_on')
        elif sort_type == 'plus-anciens':
            product_list = Product.objects.order_by('+post_on')
        elif sort_type == 'bas-haut':
            product_list = Product.objects.order_by('-price')
        elif sort_type == 'haut-bas':
            product_list = Product.objects.order_by('+price')
        paginator = Paginator(product_list, 12)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
        context = {"products": products}
        return render(request, self.template_name, context)


class ShopView(View):
    template_name = "core/shop.html"

    def get(self, request, *args, **kwargs):
        product_list = Product.objects.all()
        paginator = Paginator(product_list, 12)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)
        context = {}
        return render(request, self.template_name, context)


class DetailCategoryView(View):
    template_name = "core/category.html"

    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        product_list = Product.object.filter(category=category).all()
        paginator = Paginator(product_list, 12)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'category': category, 'products': products})


class ProductView(View):
    template_name = "core/product.html"

    def get(self, request, product_slug):
        product = Product.objects.get_or_404(Product, slug=product_slug)
        pictures = ProductImage.objects.filter(product=product.id)
        context = {'product': product,
                   'pictures': pictures
                   }
        return (request, self.template_name, context)


class CreateCartView(View):  # Panier
    template_name = "core/cart.html"

    def get(self, request, product_slug, qte):
        if not request.user.is_authenticated():
            if 'cart' not in request.session:
                cart = dict()
            else:
                cart = request.session['cart']

            if product_slug in cart:
                cart[product_slug] = int(cart[product_slug]) + int(qte)
            else:
                cart[product_slug] = qte

            request.session['cart'] = cart
        else:
            client = Customer.objects.get(user=request.user)
            if Order.objects.filter(customer=client.id, status='In Cart').exists():
                cart = Order.objects.get(customer=client.id, status='In Cart')
            else:
                cart = Order(customer=client.id, state='In Cart')
            if OrderItem.objects.filter(product__slug=product_slug, order=cart).exists():
                order_item = OrderItem.objects.filter(
                    product__slug=product_slug, order=cart)
                order_item.qte += int(qte)
            else:
                product = Product.objects.get(slug=product_slug)
                order_item = OrderItem(product=product.id, order=cart, qte=qte)

            cart.save()
            order_item.save()
            return render(request, self.template_name, )


class DeleteCartView(View):
    template_name = "core/cart.html"

    def get(self, request, product_slug):
        if not request.user.is_authenticated() and 'cart' in request.session:
            del request.session['cart']
        else:
            client = Customer.objects.get(user=request.user.id)
            Order(customer=client.id, state='In Cart').delete()
        return render(request, self.template_name,)


class ListCartView(View):
    template_name = "core/cart.html"

    def get(self, request, *args, **kwargs):
        cart = None
        order_items = None
        if not request.user.is_authenticated():
            if 'cart' in request.session:
                cart = list()
                for product, qte in request.session.get('cart').iteritems():
                    order_items = OrderItem(product=product.id, qte=qte)
                    order_items.total_price += order_items.total()
                    list.append(cart, order_items)
        else:
            cart = Order.objects.filter(
                customer=request.user.id, state='In Cart')
            if cart.exist():
                order_items = OrderItem.objects.filter(order=cart.id)
                for item in order_items:
                    order_items.total_price += item.total()

        context = {'cart': cart,
                   'order_items': order_items
                   }
        return render(request, self.template_name, context=context)


class CheckoutView(View):  # Formulaire validation commande
    template_name = "core/checkout.html"
    form_class = CheckoutForm

    def get(self, request, order_id):
        form = self.form_class()
        cart = None
        order_items = None
        if not request.user.is_authenticated():
            if 'cart' in request.session:
                cart = list()
                for product, qte in request.session.get('cart').iteritems():
                    order_items = OrderItem(product=product.id, qte=qte)
                    order_items.total_price += order_items.total()
                    list.append(cart, order_items)
            return render(request, self.template_name, {'form': form})
        else:
            client = Customer.objects.get(user=request.user)
            if client.adress:
                instance = Address.objects.get(id=client.adress)
                form = self.form_class(request.GET, initial={
                                       'city': instance.city,
                                       'street': instance.street,
                                       'phone': instance.phone,
                                       'full_name': instance.full_name,
                                       'note': ''})
            cart = Order.objects.filter(
                customer=request.user.id, state='In Cart')
            if cart.exist():
                order_items = OrderItem.objects.filter(order=cart.id)
                for item in order_items:
                    order_items.total_price += item.total()
        context = {'cart': cart,
                   'order_items': order_items
                   }
        return render(request, self.template_name, {'form': form})

    def post(self, request, order_id):
        if not request.user.is_authenticated():
            form = self.form_class(request.POST)
            if form.is_valid():
                return render(request, self.template_name, {'form': form})


class PaymentView(View):
    template_name = "core/payment.html"

    def get(self, request, *args, **kwargs):
        pass


class Login(View):
    template_name = "core/login.html"

    def post(self, request, *args, **kwargs):

        valuenext = request.GET.get("next", "/")
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(valuenext)
            else:
                error = ValidationError("Invalid email or password")
                context = {"form": form, "error": error}
                print(form.errors)
                return render(request, self.template_name, context)
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class SignupView(TemplateView):
    template_name = "core/signup.html"
    form_class = CustomerForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # on cree un compte
            customer = form.save()
            print(customer)
            # envoie d'un mail a l'utilisateur
            user_account = customer.user
            mail_subject = "Inscription réussie"
            to_email = [
                user_account.email,
            ]
            current_site = get_current_site(request)
            html_message = render_to_string(
                "core/mail_template.html",
                {"user": user_account, "domain": current_site.domain},
            )
            plain_message = strip_tags(html_message)
            send_mail(
                mail_subject,
                plain_message,
                "FindInvest info <stage-dev@yaknema.com>",
                to_email,
                fail_silently=False,
                html_message=html_message,
            )
            # connexion de l'utilisateur directement sur la plateforme
            user = authenticate(email=user_account.email,
                                password=user_account.password)
            if user is not None:
                login(request, user)
                return redirect("core:home")
            else:
                error = ValidationError("Invalid email or password")
                context = {"form": form, "error": error}
                return render(request, self.template_name, context)
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


class SearchView(View):
    template_name = "core/search.html"

    def post(self, request,  *args, **kwargs):
        searched = request.POST["searched"]
        results = Product.objects.filter(slug__icontains=searched)
        nbre = len(results)
        paginator = Paginator(results, 9)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)

        context = {
            "searched": searched,
            "nbre": nbre,
            "products": products,
        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
