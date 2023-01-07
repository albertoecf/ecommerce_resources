from django.contrib import admin
from .models import ProductClass
# Register your models here.


class ProductAdminClass(admin.ModelAdmin):
    """Customizes the display and behavior of the `Product` model in the Django admin interface.

    Attributes:
        list_display (tuple): A tuple of field names to display in the list view of the model.
        prepopulated_fields (dict): A dictionary mapping field names to the fields that should be used to
            prepopulate them"""
    list_display = ('product_name', 'price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(ProductClass, ProductAdminClass)
