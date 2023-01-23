from django.db import models
from app_accounts.models import AccountClass
from app_store.models import ProductClass, VariationClass

# Create your models here.

class PaymentClass(models.Model):
    user = models.ForeignKey(AccountClass, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class OrderClass(models.Model):
    STATUS = {
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    }

    user = models.ForeignKey(
        AccountClass, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        PaymentClass, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderProductClass(models.Model):
    order = models.ForeignKey(OrderClass, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        PaymentClass, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AccountClass, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductClass, on_delete=models.CASCADE)
    variation = models.ForeignKey(VariationClass, on_delete=models.CASCADE)
    color= models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    quantity= models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
