from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('profile/', views.user_home, name='user_home'),
    path('profile/suppliers/', views.suppliers, name='suppliers'),
    path('profile/suppliers/add_supplier', views.add_supplier, name='add_supplier'),
    path('newshop/', views.add_shop, name='add_shop'),
    path('shophome/<slug:shop_name>', views.category_home, name='shop_home'),
    path('manageitems/<slug:shop_name>', views.manageitems, name='manageitems'),
    path('shophome/<slug:shop_name>/add_product', views.add_product, name='add_product'),
    path('addcategory', views.add_category, name='add_category'),
]
