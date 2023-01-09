from django.contrib import admin
from .models import CartClass, CartItemClass
# Register your models here.

admin.site.register(CartClass)
admin.site.register(CartItemClass)
