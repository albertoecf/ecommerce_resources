from django.urls import path
from . import views

app_name = 'app_store'
urlpatterns = [
    path('', views.store_view, name='store_view_path'),
    path('<slug:category_slug>', views.store_view, name='products_by_category_path')
]
