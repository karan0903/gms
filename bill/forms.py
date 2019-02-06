from django import forms

from management.models import Product, Category

class BillForm(forms.Form):
    product =  forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField()
