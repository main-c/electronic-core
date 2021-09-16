from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from core.forms import LoginForm, CustomerForm, AdressForm, CheckoutForm, UpdateCartForm
from django.contrib.auth import authenticate, login, logout
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from core.models import (Product, ProductImage,
                         Category, Customer, OrderItem, Order, Address)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(View):
    template_name = "core/home.html"

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
        context = {'products': products}
        return render(request, self.template_name, context)


class CartView(TemplateView):
    template_name = "core/cart.html"


class AccountView(TemplateView):  # Dashboard
    template_name = "core/account.html"


class FilterProductView(View):
    template_name = "core/sale.html"

    def get(self, request, sort_type):
        product_list = Product.objects.all().prefetch_related('produit')
        if sort_type == 'on-solde':
            product_list = Product.objects.filter(
                status="On Sale").all().prefetch_related('produit')
        elif sort_type == 'new':
            product_list = Product.objects.filter(
                status="New").all().prefetch_related('produit')
        elif sort_type == 'price' and request.POST['price']:
            products_list = Product.objects.filter(
                price=request.POST['price']).all().prefetch_related('produit')

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
        product_list = Product.objects.all().prefetch_related('produit')
        if sort_type == 'plus-recents':
            product_list = Product.objects.order_by(
                '-post_on').prefetch_related('produit')
        elif sort_type == 'plus-anciens':
            product_list = Product.objects.order_by(
                '+post_on').prefetch_related('produit')
        elif sort_type == 'bas-haut':
            product_list = Product.objects.order_by(
                '-price').prefetch_related('produit')
        elif sort_type == 'haut-bas':
            product_list = Product.objects.order_by(
                '+price').prefetch_related('produit')
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
        product_list = Product.objects.all().prefetch_related('images')
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
        context = {'products': products}
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
        product = Product.objects.get_or_404(
            Product, slug=product_slug).prefetch_related('produit')
        pictures = ProductImage.objects.filter(product=product.id)
        context = {'product': product,
                   'pictures': pictures
                   }
        return (request, self.template_name, context)


class CreateCartView(View):  # Panier
    template_name = "core/home.html"

    def get(self, request, product_slug, qte=0):
        if not request.user.is_authenticated:
            pass
            """if 'cart' not in request.session:
                    cart = dict()
                else:
                    cart = request.session['cart']

                if product_slug in cart:
                    cart[product_slug] = int(cart[product_slug]) + int(qte)
                else:
                    cart[product_slug] = qte

                request.session['cart'] = cart"""
        else:
            client = Customer.objects.get(user=request.user)
            product = Product.objects.get(slug=product_slug)
            if Order.objects.filter(customer=client, state='In Cart').exists():
                cart = Order.objects.get(customer=client, state='In Cart')
            else:
                cart = Order(customer=client, state='In Cart')
            if OrderItem.objects.filter(product__slug=product_slug, order=cart).exists():
                order_item = OrderItem.objects.get(
                    product__slug=product_slug, order=cart)
                order_item.qte += 1
                order_item.product.qte -= 1
                order_item.total_price = order_item.total()
                cart.price += product.price
            else:
                order_item = OrderItem(product=product, order=cart, qte=1)
                order_item.total_price = order_item.total()
                order_item.decrease_product_qte()
                cart.price += product.price

            cart.save()
            order_item.save()
            context = {"len_cart": cart.article_qty()}
            return redirect('core:home')


class DeleteItemView(View):
    template_name = "core/cart.html"

    def get(self, request, product_slug):
        if not request.user.is_authenticated and 'cart' in request.session:
            del request.session['cart']
        else:
            client = Customer.objects.get(user=request.user.id)
            cart = Order.objects.filter(customer=client.id, state='In Cart')[0]
            order_item = cart.items.filter(product__slug=product_slug)[0]
            cart.price -= order_item.total_price
            order_item.delete()
            cart.save()
        return redirect('core:list_cart')


class DeleteCartView(View):
    template_name = "core/cart.html"

    def get(self, request, order_id):
        if not request.user.is_authenticated and 'cart' in request.session:
            del request.session['cart']
        else:
            cart = Order.objects.filter(id=order_id)[0]
            cart.delete()
        return redirect('core:list_cart')


"""class UpdateCartView(View):
    template_name = "core/cart.html"
    form_class = UpdateCartForm

    def get(self, request, *args, **kwargs):
        cart = None
        order_items = None
        if not request.user.is_authenticated:
            if 'cart' in request.session:
                cart = list()
                for product, qte in request.session.get('cart').iteritems():
                    order_items = OrderItem(product=product.id, qte=qte)
                    order_items.total_price += order_items.total()
                    list.append(cart, order_items)
        else:
            cart = Order.objects.filter(
                customer=request.user.customer, state='In Cart')[0]
            order_items = cart.items.all()
        context = {'cart': cart,
                   'order_items': order_items
                   }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        order_item_id = form.cleaned_data.get('order_item_id')
        qte = form.cleaned_data.get('qte')
        if form.is_valid:
            order_item = get_object_or_404(OrderItem, id=order_item_id)
            order_item.qte += qte
            context = {}
            if order_item.qte > order_item.product.qte:
                error_message = 'Limites des stocks atteints'
                order_item.qte = order_item.product.qte
                context = {"error_message": error_message}
            context['qte'] = order_item.qte
            return render(self, self.template_name, context)
"""


class ListCartView(View):
    template_name = "core/cart.html"
    context = {}

    def get(self, request, *args, **kwargs):
        cart = None
        order_items = None
        if not request.user.is_authenticated:
            if 'cart' in request.session:
                cart = list()
                for product, qte in request.session.get('cart').iteritems():
                    order_items = OrderItem(product=product.id, qte=qte)
                    order_items.total_price += order_items.total()
                    list.append(cart, order_items)
        else:
            client = Customer.objects.get(user=request.user.id) 
            cart = Order.objects.filter(customer=client, state='In Cart').first()
            if cart:
                order_items = cart.items.all()
                self.context = {'cart': cart, 'order_items': order_items}
                return render(request, self.template_name, self.context)
            else:
                return render(request, self.template_name, {'error_message': "Panier Vide"})


class CheckoutView(View):  # Formulaire validation commande
    template_name = "core/checkout.html"
    form_class = CheckoutForm
    context = {}
    
    def get(self, request, order_id):
        form = self.form_class()
        cart = None
        order_items = None
        client = Customer.objects.get(user=request.user)
        if client.adress:
            instance = Address.objects.get(id=client.adress)
            self.context['instance'] = instance
        cart = Order.objects.filter(
            customer=client, state='In Cart').first()
        if cart:
            order_items = OrderItem.objects.filter(order=cart.id)
            for order in order_items:
                order_items.total_price += item.total()
        self.context['cart'] = cart
        self.context['order_items'] = order_items
        self.context['form'] = form

        return render(request, self.template_name, self.context)

    def post(self, request, order_id):
        client = Customer.objects.get(user=request.user)
        cart = Order.objects.filter(
            customer=request.client, state='In Cart').first()
        form = self.form_class(data=request.POST)
        if form.is_valid():
            address = form.save()
            client.address = address
            cart.note = form.cleaned_data['note']
            client.save()
            address.save(commit=True)
            cart.save()
            return render(request, self.template_name)



class PaymentView(View):
    template_name = "core/payment.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)



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
