from django.urls import path
from . import views
app_name = 'app_accounts'
urlpatterns = [
    path('register/',views.register_view, name='register_view_path'),
    path('login/',views.login_view, name='login_view_path'),
    path('logout/',views.logout_view, name='logout_view_path'),
    ]
