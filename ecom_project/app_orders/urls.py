from django.urls import path
from . import views
app_name = 'app_orders'
urlpatterns = [
    path('place_order/', views.place_order_view, name='place_order_view_path'),
    path('payments/', views.payments_view, name='payments_view_path'),
    path('order_completed/', views.order_completed_view, name='order_completed_view_path'),
    ]
