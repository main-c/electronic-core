from django.contrib import admin
from core.models import *


class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'full_name', 'phone')
    search_fields = ('city', 'full_name')


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'adress', 'newsletter_id')
    search_fields = ('user__last_name', 'user__email')


class PhotoInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'qte', 'status', 'category_id',)
    list_filter = ('title', 'status', 'category_id', 'price')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        PhotoInline
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'price', 'ordered_on', 'state',)
    list_filter = ('ordered_on', 'customer_id')
    search_fields = ('customer_id',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'qte', 'order', 'total_price',)
    list_filter = ('product', 'order', 'total_price')
    search_fields = ('product__title',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_mode', 'token', 'amount', 'paid_on',)
    list_filter = ('payment_mode', 'paid_on', 'customer_id')
    search_fields = ('paid_on',)


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'add_on', 'product_id')
    list_filter = ('feedback', 'add_on', 'product_id')
    search_fields = ('feedback', 'add_on', 'product_id')


admin.site.register(Address, AddressAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FeedBack, FeedBackAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
