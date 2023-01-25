from django.contrib import admin
from .models import PaymentClass, OrderClass, OrderProductClass
# Register your models here.


class OrderAdminClass(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email',
                    'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name',
                     'last_name', 'phone', 'email']
    list_per_page = 20


admin.site.register(PaymentClass)
admin.site.register(OrderClass, OrderAdminClass)
admin.site.register(OrderProductClass)
