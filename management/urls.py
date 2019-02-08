from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('profile/', views.user_home, name='user_home'),
    path('profile/suppliers/', views.suppliers, name='suppliers'),
    path('profile/suppliers/add', views.add_supplier, name='add_supplier'),
    path('shops/add/', views.add_shop, name='add_shop'),
    path('shops/<slug:shop_name>', views.category_home, name='shop_home'),
    path('shops/<slug:shop_name>/products/add', views.add_product, name='add_product'),
    path('bill/<int:shop_id>', views.bill_page, name='bill'),
    path('get_data/<search_type>/<search_string>/', views.get_customer_products, name='get_data'),
    path('add_customer/', views.add_customer, name='addcustomer'),
    path('shops/<slug:shop_name>/addexpense/', views.add_expense, name='add_expense'),
    path('shops/<slug:shop_name>/profit&loss/', views.profit_loss, name='profit_loss'),
]
