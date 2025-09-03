from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category-list'),
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('inventory/', views.inventory_list, name='inventory-list'),
    path('orders/', views.create_order, name='create-order'),
    path('orders/', views.order_list, name='order-list'),
    path('checkout/cbe/', views.checkout_cbe, name='checkout-cbe'),
    path('checkout/telebirr/', views.checkout_telebirr, name='checkout-telebirr'),
    path('contact/', views.contact_submit, name='contact-submit'),
]