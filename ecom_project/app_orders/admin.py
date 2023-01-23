from django.contrib import admin
from .models import PaymentClass, OrderClass , OrderProductClass
# Register your models here.

admin.site.register(PaymentClass)
admin.site.register(OrderClass)
admin.site.register(OrderProductClass)
