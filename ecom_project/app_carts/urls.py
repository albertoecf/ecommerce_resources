from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart_view_path'),
    path('add_cart/<int:product_id>',
         views.add_cart_view, name='add_cart_view_path'),
    path('remove_cart/<int:product_id>',
         views.remove_unit_item_from_cart, name='remove_cart_view_path'),
    path('remove_item_from_cart/<int:product_id>',
         views.remove_item_from_cart, name='remove_item_from_cart_view_path'),
    path('checkout/', views.checkout_view, name='checkout_view_path'),
]
