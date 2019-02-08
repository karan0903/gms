from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('profile/', views.user_home, name='user_home'),
    path('profile/suppliers/', views.suppliers, name='suppliers'),
    path('profile/suppliers/add', views.add_supplier, name='add_supplier'),
    path('shops/add/', views.add_shop, name='add_shop'),
    path('shops/<slug:shop_name>', views.category_home, name='shop_home'),
    # path('manageitems/<slug:shop_name>', views.manageitems, name='manageitems'),
    path('shops/<slug:shop_name>/products/add', views.add_product, name='add_product'),
    # path('addcategory', views.add_category, name='add_category'),
]
