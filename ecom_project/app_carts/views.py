from django.shortcuts import render, redirect
from app_store.models import ProductClass
from .models import CartClass, CartItemClass

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
def cart_view(request):
    return render(request, 'store/cart.html')
