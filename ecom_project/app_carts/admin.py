from django.contrib import admin
from .models import CartClass, CartItemClass
# Register your models here.
class CartAdminClass(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

class CartItemAdminClass(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')

admin.site.register(CartClass, CartAdminClass)
admin.site.register(CartItemClass,CartItemAdminClass )
