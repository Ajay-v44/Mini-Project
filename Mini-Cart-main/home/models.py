from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import admin
from django import forms
# Create your models here.


class DeliveryAddress(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(unique=True)
    altmob = models.IntegerField(unique=True)
    pincode = models.IntegerField()
    address = models.TextField()
    dtype = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.username} - {self.address}"

    class Meta:
        db_table = 'DeliveryAddress'


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('username', 'mobile', 'altmob', 'pincode',
                    'address', 'dtype', 'state', 'country')
    # Assuming 'username' is a ForeignKey to User
    search_fields = ['username__username']
    list_filter = ['country']


class Products(models.Model):
    pro_name = models.CharField(max_length=150)
    pro_desc = models.CharField(max_length=250)
    pro_price = models.IntegerField()
    category = models.CharField(max_length=150)
    pro_brand = models.CharField(max_length=150)
    pro_rating = models.FloatField()
    pro_image = models.ImageField(
        upload_to='uploads', height_field=None, width_field=None, max_length=None)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pro_name} - {self.pro_desc}"

    class Meta:
        db_table = 'Products'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('pro_name', 'pro_desc', 'pro_price', 'category',
                    'pro_brand', 'pro_rating', 'is_available', 'pro_image')
    search_fields = ['pro_name']
    list_filter = ['category', 'pro_brand']


class Cart(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()

    def __str__(self):
        return f"{self.username}"


class DeliverProducts(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    orderd_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    paymentmod = models.CharField(max_length=50, default="COD")
    total_amount = models.IntegerField()
    Status = models.CharField(max_length=50, default="pending")
    deliveron = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.username} - {self.product}"

    class Meta:
        db_table = 'DeliverProducts'


@admin.register(DeliverProducts)
class DeliverProductsAdmin(admin.ModelAdmin):
    list_display = ('username', 'product', 'orderd_at', 'quantity',
                    'paymentmod', 'total_amount', 'Status', 'deliveron')
    search_fields = ['username__username']
    list_filter = ['Status', 'deliveron']
    list_editable = ['Status']

    formfield_overrides = {
        models.CharField: {'widget': forms.Select(choices=[('dispatched', 'Dispatched'), ('delivered', 'Delivered')])},
    }


class Blogs(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    postedate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    image = models.ImageField(upload_to='uploads')

    def __str__(self):
        return f"{self.title}"


class Reviews(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    postedon = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.review}"


class Contactus(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        db_table = 'Contactus'


@admin.register(Contactus)
class ContactusAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message',)
    search_fields = ['name']
    list_filter = ['message']
