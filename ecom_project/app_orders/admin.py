from django.contrib import admin
from .models import PaymentClass, OrderClass, OrderProductClass
# Register your models here.


class OrderProductInLineClass(admin.TabularInline):
    model = OrderProductClass
    readonly_fields = ('payment', 'user', 'product',
                       'quantity', 'product_price')
    extra = 0


class OrderAdminClass(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email',
                    'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered', 'first_name']
    search_fields = ['order_number', 'first_name',
                     'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInLineClass]


admin.site.register(PaymentClass)
admin.site.register(OrderClass, OrderAdminClass)
admin.site.register(OrderProductClass)
