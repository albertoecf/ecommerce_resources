from django.db import models
from app_store.models import ProductClass

# Create your models here.

class CartClass(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.cart_id

class CartItemClass(models.Model):
    """Product which was selected and will be buy (or not) in the future"""
    product = models.ForeignKey(ProductClass, on_delete = models.CASCADE)
    cart = models.ForeignKey(CartClass, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def subtotal(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
