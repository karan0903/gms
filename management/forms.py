from django import forms
from django.contrib.auth.models import User
from management.models import Shop, Category, Product, Supplier, Customer, Bill


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

#
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ('product', 'mfg_date', 'exp_date', 'buying_price', 'selling_price', 'quantity_reamins', 'supplier',)
