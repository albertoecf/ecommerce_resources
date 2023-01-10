from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart_view, name='cart_view_path'),
    path('add_cart/<int:product_id>',views.add_cart_view, name='add_cart_view_path'),
]
