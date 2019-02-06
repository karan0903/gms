from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('profile/', views.user_home, name='user_home'),
    path('newshop/', views.add_shop, name='add_shop'),
    path('shophome/<slug:shop_name>', views.shop_home, name='shop_home'),
    path('manageitems/<slug:shop_name>', views.manageitems, name='manageitems'),
    path('addcategory', views.add_category, name='add_category'),
    path('categoryhome/<slug:category_name>', views.category_home, name='category_home'),
    path('addproduct', views.add_product, name='add_product'),
    # path('/user', include('shop.urls')),
]
