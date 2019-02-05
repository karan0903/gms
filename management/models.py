from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)


class Supplier(models.Model):
    supplier = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = PhoneNumberField(null=False, blank=False, unique=True)


class Product(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    mfg_date = models.DateField(("Date"), default=timezone.now)
    exp_date = models.DateField(("Date"), default=timezone.now)
    buying_price = models.FloatField(null=True, blank=True, default=None)
    selling_price = models.FloatField(null=True, blank=True, default=None)
    quantity_remains = models.FloatField(null=True, blank=True, default=None)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    minimum_limit = models.FloatField(null=True, blank=True, default=None)


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)


class Bill(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    selling_price = models.FloatField(null=True, blank=True, default=None)
    quantity = models.FloatField(null=True, blank=True, default=None)

    @property
    def total_price(self):
        return self.selling_price * self.quantity
