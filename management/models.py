from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    
    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(unique=True, max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    mfg_date = models.DateField(("Date"), default=timezone.now)
    exp_date = models.DateField(("Date"), default=timezone.now)
    buying_price = models.FloatField( default=None)
    selling_price = models.FloatField( default=None)
    quantity_remains = models.FloatField( default=None)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    minimum_quantity = models.FloatField( default=None)

    def __str__(self):
        return self.name
    


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 150)
    phone_number = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)


class Bill(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    selling_price = models.FloatField( default=None)
    quantity = models.FloatField( default=None)

    def __self__(self):
        return self.product

    @property
    def total_price(self):
        return self.selling_price * self.quantity


class Expense(models.Model):
    employee_expense = models.FloatField(default=0)
    travel_expense = models.FloatField(default=0)
    additional_expense = models.FloatField(default=0)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    date = models.DateTimeField(("Date"), default=datetime.date.today)

    @property
    def total_expense(self):
        return self.employee_expense + self.travel_expense + self.additional_expense