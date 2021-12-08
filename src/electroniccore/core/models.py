from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField


class Address(models.Model):
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, null=True)
    phone = models.BigIntegerField(null=True)

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.city} - {self.street}'


class Newsletter(models.Model):
    email = models.EmailField()


class Customer(models.Model):

    user = models.OneToOneField(User, models.CASCADE, related_name='customer')
    adress = models.OneToOneField(Address, models.CASCADE, null=True)
    newsletter_id = models.ForeignKey(
        Newsletter, models.SET_NULL, null=True, default=None)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f'{self.user.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):

    STATUS = (
        ('New', 'New'),
        ('On Sale', 'On Sale'),
        ('Reached Limits', 'Reached Limits')
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.IntegerField()
    full_desc = QuillField(default='', null=True, blank=True)
    mini_desc = QuillField(default='', null=True, blank=True)
    qte = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    post_on = models.DateField(auto_now=True)
    category_id = models.ForeignKey(Category, models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    def get_main_image(self):
        return self.images.get(title='main').image.url


class ProductImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products_image')
    product = models.ForeignKey(Product, models.CASCADE, related_name='images')

    def get_main_image(self):
        return self.filter(title='main')


class Order(models.Model):
    STATE = (
        ('Validated', 'Validated'),
        ('In Cart', 'In Cart'),
        ('Paid', 'Paid'),
    )
    note = models.TextField(null=True)
    ordered_on = models.DateTimeField(auto_now=True, null=True)
    price = models.IntegerField(default=0)
    adress = models.ForeignKey(Address, models.CASCADE, null=True)
    state = models.CharField(max_length=100, choices=STATE, default=STATE[1])
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True,)

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

    def __str__(self):
        return f'commande de {self.customer.user.last_name}'

    


class OrderItem(models.Model):
    qte = models.IntegerField()
    total_price = models.IntegerField(default=0)
    order = models.ForeignKey(Order, models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, models.CASCADE)

    def total(self):
        return (self.product.price * self.qte)

    def decrease_product_qte(self):
        self.product.qte -= 1


class Payment(models.Model):
    payment_mode = models.CharField(max_length=200,)
    token = models.CharField(max_length=200)
    amount = models.IntegerField()
    paid_on = models.DateTimeField(auto_now=True)
    customer_id = models.ForeignKey(Customer, models.SET_NULL, null=True)
    order_id = models.OneToOneField(Order, models.CASCADE)


class FeedBack(models.Model):
    feedback = models.TextField()
    add_on = models.DateTimeField(auto_now=True)
    product_id = models.OneToOneField(Product, models.CASCADE)

    def __str__(self):
        return f'avis sur le produit {self.product_id.title}'
