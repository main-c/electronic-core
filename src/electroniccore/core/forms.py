from django import forms
from django.contrib.auth.models import User
from django.forms import fields, models
from core.models import (Adress, Newsletter, Customer, Category, Product,
                         ProductImage, Order, Payment, FeedBack)


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')


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
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already used.")
        return email

    def save(self, commit=True):
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User.objects.create(
            last_name=last_name,
            email=email,
            password=password,

        )
        user.set_password(self.cleaned_data["password"])
        customer = Customer.objects.create(
            user=user,)
        return customer


class AdressForm(forms.ModelForm):

    class Meta:
        model = Adress
        fields = ('city', 'street', 'full_name', 'phone')


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=200, required=True)
    street = forms.CharField(max_length=200, required=True)
    note = forms.CharField(widget=forms.Textarea())
    phone = forms.NumberInput()
    policy = forms.CharField(widget=forms.CheckboxInput())

    class Meta:
        fields = ('city', 'street', 'full_name', 'phone', 'note', 'policy')
