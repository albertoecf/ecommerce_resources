from .models import CartClass, CartItemClass
from .views import _cart_id

def counter(request):
    cart_items_count = 0

    try :
        cart_fetched = CartClass.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_items = CartItemClass.objects.all().filter(user=request.user)
        else:
            cart_items = CartItemClass.objects.all().filter(cart = cart_fetched[ :1])

        # We want the sum of all items (item_id * quantity)
        for cart_item in cart_items:
            cart_items_count  += cart_item.quantity

    except CartClass.DoesNotExist:
            cart_items_count = 0

    return dict(cart_items_count=cart_items_count)
