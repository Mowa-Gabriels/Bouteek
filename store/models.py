from itertools import product
from sre_parse import State
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_digital = models.BooleanField(default=False, null=True, blank=False)
    is_available = models.BooleanField(default=True, null=True, blank=False)
    display_image = models.ImageField(blank = True, null= True)
    sub_image_1 = models.ImageField(blank = True, null= True)
    sub_image_2 = models.ImageField(blank = True, null= True)
    sub_image_3 = models.ImageField(blank = True, null= True)
    sub_image_4 = models.ImageField(blank = True, null= True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.display_image.url
        except:
            url =''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True)


    def __str__(self):
        return self.customer.name

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, default=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}(s) by {} on {}".format(self.quantity, self.product.name, self.order.customer.name, self.date_added)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city =  models.CharField(max_length=255, blank=True, null=True)
    state =  models.CharField(max_length=255, blank=True, null=True)
    zipcode =  models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.customer.name, self.address)
