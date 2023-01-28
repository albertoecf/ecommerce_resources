from django.urls import path
from . import views
app_name = 'app_accounts'
urlpatterns = [
    path('register/', views.register_view, name='register_view_path'),
    path('login/', views.login_view, name='login_view_path'),
    path('logout/', views.logout_view, name='logout_view_path'),
    path('', views.dashboard_view, name='dashboard_view_path'),
    path('forgot_password/', views.forgot_password_view,
         name='forgot_password_view_path'),
    path('reset_password_validate/<uidb64>/<token>/',
         views.reset_password_validate_view, name='reset_password_validate_view_path'),
    path('reset_password/', views.reset_password_view,
         name='reset_password_view_path'),
    path('activate/<uidb64>/<token>',
         views.activate_view, name='activate_view_path'),
    path('my_orders/', views.my_orders_view, name='my_orders_view_path'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile_view_path'),
    path('change_password/', views.change_password_view, name='change_password_view_path'),

]
