from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.users_list_views, name='user_list'),
]
