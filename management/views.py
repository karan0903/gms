from django.shortcuts import render
from .forms import ShopForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from management.models import Shop, Category, Product, Supplier, Customer, Bill
from django.http import HttpResponse


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


@login_required
def shop_home(request, shop_name):
    # return HttpResponse('ok'+str(shop_name))
    shop = Shop.objects.filter(name=shop_name)
    print(shop)
    return render(request, 'management/shophome.html', {'shop': shop})


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
            print(shops)
            shops = Shop.objects.filter(owner=request.user)
            if len(shops) > 0:
                return render(request, 'management/user.html', {'shops': shops})
            else:
                return render(request, 'management/user.html')


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
def category_home(request, category_name):
    # category_name = Category.objects.filter(name=category_name)
    products = Product.objects.all()
    # print(products)
    # return HttpResponse('ok'+str(category_name))
    # # print(shop)
    return render(request, 'management/products.html', {'products': products})


@login_required
def add_product(request):
    return HttpResponse('ok')
