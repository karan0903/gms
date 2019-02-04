from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

class Product(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('Category', models.DO_NOTHING, blank=True, null=True)

class Supplier(models.Model):
    supplier = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = PhoneNumberField(null=False, blank=False, unique=True)

class Item(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    mfg_date = models.DateField(("Date"), default=timezone.now)
    exp_date = models.DateField(("Date"), default=timezone.now)
    buying_price = models.FloatField(null=True, blank=True, default=None)
    selling_price = models.FloatField(null=True, blank=True, default=None)
    quantity_reamins = models.FloatField(null=True, blank=True, default=None)
    supplier = models.ForeignKey('Supplier', models.DO_NOTHING, blank=True, null=True)


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)

class Bill(models.Model):
    bill_item = models.ForeignKey('BillItem', models.DO_NOTHING, blank=True, null=True)

class BillItem(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    selling_price = models.FloatField(null=True, blank=True, default=None)
    quantity = models.FloatField(null=True, blank=True, default=None)
    total_price = models.FloatField(null=True, blank=True, default=None)

class CustomerBill(models.Model):
    date = models.DateField(("Date"), default=timezone.now)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    bill = models.ForeignKey('Bill', models.DO_NOTHING, blank=True, null=True)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    total_price = models.FloatField(null=True, blank=True, default=None)

class BillHistory(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', models.DO_NOTHING, blank=True, null=True)
    cutomerbill = models.ForeignKey('BillHistory', models.DO_NOTHING, blank=True, null=True)