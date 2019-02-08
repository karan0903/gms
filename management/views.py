from django.shortcuts import render
from .forms import ShopForm, CategoryForm, ProductForm, SupplierForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from management.models import Shop, Category, Product, Supplier, Customer, Bill
from django.http import HttpResponse
from django.shortcuts import redirect


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
def update_db(request):
    pass


