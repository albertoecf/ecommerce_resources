from django import forms
from .models import OrderClass


class OrderFormClass(forms.ModelForm):
    class Meta:
        model = OrderClass
        fields = ['first_name', 'last_name', 'email', 'address_line_1',
                 'address_line_2', 'province', 'country', 'city', 'order_note']
