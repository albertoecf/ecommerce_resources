from django.shortcuts import render, redirect, get_object_or_404
from app_store.models import ProductClass, VariationClass
from .models import CartClass, CartItemClass
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# We need a local only function -> def _name_of_the_function
def _cart_id(request):
    """ Generates a cart id for the current session if one does not already exist.
    If running as main script, returns the cart id. Otherwise, does nothing.

    Parameters:
    request (HttpRequest): The request object containing the current session.

    Returns:
    cart"""
    cart = request.session.session_key
    if not cart:
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
    # look for specific product in our database
    product = ProductClass.objects.get(id=product_id)

    current_user = request.user

    if current_user.is_authenticated:
        #here should be the logic of authenticated user
        product_variation = []


        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = VariationClass.objects.get(
                        product=product,
                        variationclasss_category__iexact=key,
                        variationclass_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass



        is_cart_item_exists  = CartItemClass.objects.filter(product=product, user=current_user).exists()


        if is_cart_item_exists:
            cart_items = CartItemClass.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in cart_items :
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItemClass.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()
            else :
                item = CartItemClass.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variationclass.clear()
                    item.variationclass.add(product_variation)
                item.save()
        else:
            cart_item = CartItemClass.objects.create(
                product=product,
                quantity=1,
                user = current_user,
            )
            if len(product_variation)> 0:
                cart_item.variationsclass.clear()
                cart_item.variationsclass.add(product_variation)
            cart_item.save()
        return redirect('cart_view_path')

    else :
        product_variation = []


        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = VariationClass.objects.get(
                        product=product,
                        variationclasss_category__iexact=key,
                        variationclass_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        # do we have a cart already? if not, create one
        try:
            cart = CartClass.objects.get(
                cart_id=_cart_id(request))  # user current session
        except CartClass.DoesNotExist:
            cart = CartClass.objects.create(cart_id=_cart_id(request))
            cart.save()

        is_cart_item_exists  = CartItemClass.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_items = CartItemClass.objects.filter(product=product, cart=cart)

            ex_var_list = []
            id = []
            for item in cart_items :
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItemClass.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()
            else :
                item = CartItemClass.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variationclass.clear()
                    item.variationclass.add(product_variation)
                item.save()
        else:
            cart_item = CartItemClass.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if len(product_variation)> 0:
                cart_item.variationsclass.clear()
                cart_item.variationsclass.add(product_variation)
            cart_item.save()
        return redirect('cart_view_path')


def remove_unit_item_from_cart(request, product_id, cart_item_id):
    """Removes a single unit of an item from the cart for the current session.
    If the item's quantity becomes 0 after removing a unit, the item is removed
    from the cart completely.

    Parameters:
    request (HttpRequest): The request object containing the current session.
    product_id (int): The id of the product to remove from the cart.
    cart_item_id (int): The id of the cart item to remove the unit from.

    Returns:
    None"""
    current_user = request.user
    cart_item = get_object_or_404(CartItemClass, id=cart_item_id)
    if cart_item.product.id == product_id and cart_item.user == current_user:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_view_path')



def remove_item_from_cart(request, product_id):
    product = get_object_or_404(ProductClass, id=product_id)
    current_user = request.user
    if current_user.is_authenticated:
        cart_item = CartItemClass.objects.filter(product=product, user=current_user)
    else:
        cart_id = _cart_id(request)
        cart_item = CartItemClass.objects.filter(product=product, cart__cart_id=cart_id)

    if cart_item.exists():
        cart_item.delete()
    return redirect('cart_view_path')



def cart_view(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItemClass.objects.filter(user=request.user, is_active=True)
        else:
            # We check if we have some current/existing cart in our database
            cart = CartClass.objects.get(cart_id=_cart_id(request))
            # If we have that cart, we want its items
            cart_items = CartItemClass.objects.filter(
                cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        # this will be only excecuted whrn object does not exist
        pass

    context_to_send = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context_to_send)


@login_required(login_url='app_accounts:login_view_path')
def checkout_view(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        # We check if we have some current/existing cart in our database
        cart = CartClass.objects.get(cart_id=_cart_id(request))
        # If we have that cart, we want its items
        cart_items = CartItemClass.objects.filter(
            cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        # this will be only excecuted whrn object does not exist
        pass

    context_to_send = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/checkout.html', context_to_send)
