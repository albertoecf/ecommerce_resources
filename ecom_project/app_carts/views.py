from django.shortcuts import render, redirect, get_object_or_404
from app_store.models import ProductClass
from .models import CartClass, CartItemClass
from django.core.exceptions import ObjectDoesNotExist


#We need a local only function -> def _name_of_the_function
def _cart_id(request):
    """ Generates a cart id for the current session if one does not already exist.
    If running as main script, returns the cart id. Otherwise, does nothing.

    Parameters:
    request (HttpRequest): The request object containing the current session.

    Returns:
    cart"""
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart

# Create your views here.
def add_cart_view(request, product_id):
    """Adds a product to the cart for the current session. If the product is already
    in the cart, increases its quantity. Otherwise, creates a new cart item with
    the specified product and quantity 1.

    Parameters:
    request (HttpRequest): The request object containing the current session.
    product_id (int): The id of the product to add to the cart.

    Returns:
    None"""
    #look for specific product in our database
    product = ProductClass.objects.get(id=product_id)
    # do we have a cart already? if not, create one
    try :
        cart = CartClass.objects.get(cart_id = _cart_id(request) ) #user current session
    except CartClass.DoesNotExist :
        cart = CartClass.objects.create(cart_id = _cart_id(request))
        cart.save()
    try:
        cart_item = CartItemClass.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItemClass.DoesNotExist:
        cart_item = CartItemClass.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart_view_path')

def remove_item_from_cart(request, product_id):
    cart_request = CartClass.objects.get(cart_id = _cart_id(request))
    product_request = get_object_or_404(ProductClass, id=product_id)
    cart_item = CartItemClass.objects.get(product=product_request, cart=cart_request)

    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else :
        cart_item.delete()

    return redirect('cart_view_path')

def remove_item_from_cart(request, product_id):
    cart_request = CartClass.objects.get(cart_id = _cart_id(request))
    product_request = get_object_or_404(ProductClass, id=product_id)
    cart_item = CartItemClass.objects.get(product=product_request, cart=cart_request)

    cart_item.delete()
    
    return redirect('cart_view_path')

def cart_view(request, total=0, quantity=0, cart_items=None):
    try:
        # We check if we have some current/existing cart in our database
        existing_cart = CartClass.objects.get(cart_id = _cart_id(request))
        # If we have that cart, we want its items
        cart_items = CartItemClass.objects.filter(cart=existing_cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        #this will be only excecuted whrn object does not exist
        pass

    context_to_send = {
                'total':total,
                'quantity':quantity,
                'cart_items':cart_items,
                'tax':tax,
                'grand_total':grand_total
    }

    return render(request, 'store/cart.html', context_to_send)
