from django.shortcuts import render
from .forms import ShopForm, CategoryForm, ProductForm, SupplierForm, ExpenseForm, ProfitLossForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from management.models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from datetime import timedelta
from django.db.models import F, Sum
import datetime


@login_required
def add_expense(request, shop_name):
   if request.method == 'GET':
       form = ExpenseForm()
       return render(request, 'management/addexpense.html', {'form': form})
   elif request.method == "POST":
       form = ExpenseForm(request.POST)
       if form.is_valid():
           shop = Shop.objects.get(name=shop_name)
           expense = form.save(commit=False)
           expense.shop = shop
           expense.save()
           return redirect('shop_home', shop_name=shop.name)


@login_required
def profit_loss(request, shop_name):
   if request.method == 'GET':
       form = ProfitLossForm()
       return render(request, 'management/addexpense.html', {'form': form})
   elif request.method == "POST":
       form = ProfitLossForm(request.POST)
       if form.is_valid():
           shop = Shop.objects.get(name=shop_name)
           data = form.cleaned_data
           x = datetime.datetime(int(data['year']), int(data['month']), 1)
           y = x + timedelta( days=29 ) 
           temp_ = BillItem.objects.filter(bill__created_at__range=(x, y), bill__shop=shop).annotate(price_diff=(F('product__selling_price') - F('product__buying_price'))*F('quantity')) 
           expense = Expense.objects.filter(date__range=(x, y), shop=shop).annotate(sum_expense=(F('travel_expense')+F('employee_expense')+F('additional_expense')))
           gain = 0
           exp = 0
           for i in temp_:
               gain += i.price_diff
           for i in expense:
               exp += i.sum_expense
           expense_set = Expense.objects.filter(date__range=(x, y), shop=shop)
           amount = gain - exp
           income_set = BillItem.objects.filter(bill__created_at__range=(x, y), bill__shop=shop).annotate(price_diff=(F('product__selling_price') - F('product__buying_price'))*F('quantity')).values('bill__created_at')
        #    print(income_set)
        #    return HttpResponse('ok')
           return render(request, 'management/profitloss.html', {'expenses': expense_set, 'income': gain, 'exp': exp, 'total':gain-exp})



def landing_page(request):
    return render(request, 'management/landing_page.html')


@login_required
def user_home(request):
    current_user = request.user
    shops = Shop.objects.filter(owner=current_user)
    if shops.count() > 0:
        return render(request, 'management/user.html', {'shops': shops})
    else:
        return render(request, 'management/user.html')


# @login_required
# def shop_home(request, shop_name):
#     # return HttpResponse('ok'+str(shop_name))
#     shop = Shop.objects.filter(name=shop_name)
#     print(shop)
#     return render(request, 'management/shophome.html', {'shop': shop})


@login_required
def manageitems(request, shop_name):
    shop_name = Shop.objects.filter(name=shop_name)
    category = Category.objects.all()
    if len(category) > 0:
        return render(request, 'management/manageitems.html', {'category': category})
    else:
        return render(request, 'management/manageitems.html')
    # return HttpResponse('ok'+str(shop_name))


@login_required
def add_shop(request):
    if request.method == 'GET': 
        form = ShopForm()
        return render(request, 'management/addshop.html', {'form': form})
    elif request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            shops = form.save(commit=False)
            shops.owner = request.user
            shops.save()
            return redirect('user_home')


@login_required
def add_category(request):
    if request.method == 'GET':
        form = CategoryForm()
        return render(request, 'management/addcategory.html', {'form': form})
    elif request.method == "POST":
        form = CategoryForm(request.POST)
        print(form)
        if form.is_valid():
            # return HttpResponse('ok')
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            print(category)
            category = Category.objects.filter(owner=request.user)
            if category.count() > 0:
                return render(request, 'management/manageitems.html', {'category': category})
            else:
                return render(request, 'management/manageitems.html')


@login_required
def category_home(request, shop_name):
    # return HttpResponse('ok'+str(shop_name))
    # category_name = Category.objects.filter(name=category_name)
    shop=Shop.objects.get(name = shop_name)
    products = Product.objects.filter(shop=shop)
    # return HttpResponse('ok'+str(shop_name))
    # # print(shop)
    return render(request, 'management/products.html', {'products': products, 'shops':shop})


@login_required
def add_product(request, shop_name):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'management/product.html', {'form': form})
    elif request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            shop = Shop.objects.get(name=shop_name)
            data = form.cleaned_data
            supplier = Supplier.objects.get(name=data['supplier'])
            category = Category.objects.get(id=1)
            product = Product()
            product.supplier = supplier
            product.shop = shop
            product.name = data['name']
            product.category = category
            product.buying_price = data['buying_price']
            product.selling_price = data['selling_price']
            product.quantity_remains = data['quantity_remains']
            product.minimum_quantity = data['minimum_quantity']
            product.save()
            return redirect('shop_home', shop_name)

@login_required
def suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'management/suppliers.html', {'suppliers': suppliers})


@login_required
def add_supplier(request):
    if request.method == 'GET':
        form = SupplierForm()
        return render(request, 'management/add_supplier.html', {'form': form})
    elif request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.save()
            return redirect('suppliers')

@login_required
@csrf_exempt
def bill_page(request, shop_id):
   if request.method == 'GET':
       try:
           shop = Shop.objects.get(pk=shop_id)
       except Shop.DoesNotExist:
           return HttpResponse('Sorry The shop doesnot exist')
       products = Product.objects.filter(shop__id=shop_id, quantity_remains__gt=0)
       return render(request, 'management/bill.html', {'products': products, 'shop':shop})
   else:
       print(request.POST)
       customer_id = request.POST.get('customer_id', '')
       items_bought = request.POST.get('items_bought','')
       items_bought = json.loads(items_bought)
       for key, value in items_bought.items():
            item_id = key
            bought_data = value
            p = Product.objects.get(pk=int(item_id))
            p.quantity_remains = int(p.quantity_remains) - int(bought_data['quantity'])
            shop = Shop.objects.get(pk=shop_id)
            # if p.quantity_remains < p.minimum_quantity:
            #     print('heymahn')
            #     body = "heymahn"
            #     supplier_mail = Supplier.objects.values('email').first()
            #     email = EmailMessage('Product order', body, to=[supplier_mail])
            #     email.send()
            #     # email = EmailMessage('Subject', 'Body', to=['your@email.com'])
            #     # email.send()
            p.save() 
            
       return JsonResponse({'status':200}, safe=False)

@login_required
def get_customer_products(request, search_type, search_string):
   if request.method == 'GET':
       customers = []
       if search_type == 'customer':
           result = Customer.objects.filter(name__icontains=search_string).all()
           for customer in result:
               customers.append({'id': customer.id, 'name':customer.name, 'number':customer.phone_number, 'address':customer.address})
           result = customers
       else:
           result = Product.objects.filter(name__icontains=search_string)
           for customer in result:
               customers.append({'id': customer.id, 'name':customer.name})
           result = customers

       return JsonResponse({'result': result }, safe=False)

@csrf_exempt
@login_required
def add_customer(request):
    if request.method == 'POST':
        customer_data = json.loads(request.POST.get('customer_data',''))
        
        if customer_data[4] == None:
            customer_data[2]=customer_data[2].replace('%40', '@') 
            c = Customer(name=customer_data[0],phone_number=customer_data[1], address=customer_data[3], email=customer_data[2])
            c.save()
        return JsonResponse({'status':200}, safe=True)

