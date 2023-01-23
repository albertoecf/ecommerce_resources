from django.urls import path
from . import views
app_name = 'app_orders'
urlpatterns = [
    path('place_order/', views.place_order_view, name='place_order_view_path'),]
