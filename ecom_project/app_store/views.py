from django.shortcuts import render, get_object_or_404
from .models import ProductClass
from app_category.models import CategoryClass
from app_carts.models import CartItemClass
from app_carts.views import _cart_id

# Create your views here.
def store_view(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None :
        # url path has category value, i.e : store/data-science
        categories = get_object_or_404(CategoryClass, slug=category_slug)
        products_available = ProductClass.objects.filter(category=categories, is_available=True)
        product_count  = products_available.count()
    else:
        products_available = ProductClass.objects.all().filter(is_available=True)
        product_count  = products_available.count()

    info_to_render = {
        'products_available' : products_available,
        'product_count' : product_count
    }
    return render(request,'store/store_file.html', info_to_render)

def product_detail_view(request, category_slug, product_slug):
    try:
        single_product = ProductClass.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItemClass.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e :
        raise e

    product_info_to_render = {
        'single_product':single_product,
        'in_cart':in_cart,
    }

    return render(request, 'store/product_detail_file.html',product_info_to_render)
