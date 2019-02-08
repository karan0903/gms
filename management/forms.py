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
class ProductForm(forms.Form):
    name = forms.CharField()
    buying_price = forms.FloatField()
    selling_price = forms.FloatField()
    quantity_remains = forms.FloatField()
    supplier = forms.CharField()
    minimum_quantity = forms.FloatField()

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields=('name','email',)


    