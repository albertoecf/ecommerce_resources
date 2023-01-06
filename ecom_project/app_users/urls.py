from django.urls import path, include
from . import views

app_name = 'app_users'
urlpatterns = [
    path('list/', views.users_list_views, name='user_list'),
]
