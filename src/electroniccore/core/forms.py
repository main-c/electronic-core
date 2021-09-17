from django import forms
from django.contrib.auth.models import User
from django.forms import fields, models
from core.models import (Address, Newsletter, Customer, Category, Product,
                         ProductImage, Order, Payment, FeedBack)


class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    class Meta:
        fields = ("username", "password")


class CustomerForm(forms.Form):
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    password = password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    class Meta:
        fields = ('last_name', 'email', 'password')

    def clean_email(self):
        email = self.data["email"]
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email already used.")
        return email

    def save(self, commit=True):
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User.objects.create_user(
            last_name=last_name,
            username=email,
            password=password,

        )
        user.set_password(self.cleaned_data["password"])
        customer = Customer.objects.create(
            user=user,)
        return customer


class AdressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('city', 'street', 'full_name', 'phone')


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=200, required=True)
    street = forms.CharField(max_length=200, required=True)
    note = forms.CharField(widget=forms.Textarea(), required=False)
    phone = forms.IntegerField(required=True)
    policy = forms.CharField(widget=forms.CheckboxInput(), required=True)

    class Meta:
        fields = ('city', 'street', 'full_name', 'phone', 'note', 'policy')

    def save(self, commit=True):
        adress = Address.objects.create(city=self.cleaned_data['city'],
                                        street=self.cleaned_data['street'],
                                        phone=self.cleaned_data['phone'],
                                        full_name=self.cleaned_data['full_name'],
                                        )
        return adress


class FilterForm(forms.Form):
    min_price = forms.IntegerField()
    max_price = forms.IntegerField()

    def clean_max_price(self):
        max_price = self.data['max_price']
        if not type(max_price) == int:
            raise forms.ValidationError("max value is not correct.")
        return max_price

    def clean_min_price(self):
        min_price = self.data['min_price']
        if  not type(max_price) == int:
            raise forms.ValidationError("min value is not correct.")
        return min_price

    class Meta:
        fields = ('min_price', 'max_price')
