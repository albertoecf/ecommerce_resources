from django.urls import path
from . import views

app_name = 'app_store'
urlpatterns = [
    path('', views.store_view, name='store_view_path'),
    path('category/<slug:category_slug>', views.store_view, name='products_by_category_path'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail_view, name = 'product_detail_path'),
    path('search/', views.search_view, name='search_view_path'),
    path('submit_review/<int:product_id>/', views.store_view, name = 'submit_review_view_path')
]
