from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_view, name='register_view_path'),
    path('login/',views.login_view, name='login_view_path'),
    path('logout/',views.logout_view, name='logout_view_path'),
    ]
