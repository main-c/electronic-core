"""from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    phone = models.BigIntegerField()


class Product(models.Model):

    STATUS = (
        ('New', 'New'),
        ('On Sale', 'On Salee'),
        ('Reached Limits', 'Reached Limits')
    )

    title = models.CharField(max_length=200)
    price = models.FloatField()
    slug = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS, default='New')


class ProductImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(upload_to='products_image')


class Order(models.Model):
    bill_to = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    note = models.TextField()
    ordered_on = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField()


class Payment(models.Model):
    pass


class Cart(models.Model):
    pass


class FeedBack(models.Model):
    pass


class Category(models.Model):
    pass


class ShippingAdress(models.Model):
    pass


class Post(models.Model):
    pass


class Comment(models.Model):
    pass
"""