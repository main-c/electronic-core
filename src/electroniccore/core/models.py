from django.db import models
from django.contrib.auth.models import User


class Adress(models.Model):
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField(null=True)


class Newsletter(models.Model):
    email = models.EmailField()


class Customer(models.Model):

    user = models.OneToOneField(User, models.CASCADE)
    adress = models.OneToOneField(Adress, models.CASCADE, null=True)
    newsleteter_id = models.ForeignKey(Newsletter, models.SET_NULL, null=True, default=None)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=250)


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
    qte = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    category_id = models.OneToOneField(Category, models.CASCADE)


class ProductImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products_image')
    product_id = models.OneToOneField(Product, models.CASCADE)


class Order(models.Model):
    STATE = (
        ('Validated', 'Validated'),
        ('In Cart', 'In Cart'),
        ('Paid', 'Paid'),
        )
    note = models.TextField(null=True)
    ordered_on = models.DateTimeField(auto_now=True, null=True)
    price = models.IntegerField(default=0)
    adress = models.ForeignKey(Adress, models.CASCADE, null=True)
    state = models.CharField(max_length=100, choices=STATE, default=STATE[1])
    customer_id = models.ForeignKey(Customer, models.SET_NULL, null=True, default=None)

    @property
    def total(self):
        total = 0
        order_items = OrderItem.objects.filter(order=self.id)
        for order_item in order_items:
            total += order_item.total()
        return total

    def article_qty(self):
        order_items = OrderItem.objects.filter(order_id=self.id)
        return len(order_items)


class OrderItem(models.Model):
    qte = models.IntegerField()
    total_price = models.IntegerField(default=0)
    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)

    def total(self):
        return (self.product.price * self.qte)


class Payment(models.Model):
    payment_mode = models.CharField(max_length=200)
    amount = models.IntegerField()
    paid_on = models.DateTimeField(auto_now=True)
    customer_id = models.ForeignKey(Customer, models.SET_NULL, null=True)
    order_id = models.OneToOneField(Order, models.CASCADE)


class FeedBack(models.Model):
    feedback = models.CharField(max_length=250)
    add_on = models.DateTimeField(auto_now=True)
    product_id = models.OneToOneField(Product, models.CASCADE)
