from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
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
        products_available = ProductClass.objects.filter(
                            category=categories, is_available=True).order_by(
                            '-created_date')
        paginator = Paginator(products_available, 6)
        page_requested = request.GET.get('page')
        paged_products = paginator.get_page(page_requested)
        product_count  = products_available.count()
    else:
        products_available = ProductClass.objects.all().filter(is_available=True).order_by('-created_date')
        paginator = Paginator(products_available, 6)
        page_requested = request.GET.get('page')
        paged_products = paginator.get_page(page_requested)
        product_count  = products_available.count()

    info_to_render = {
        'products_available' : paged_products,
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

def search_view(request):
    #are we receiving a keyword in the request?
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword:
            # we want to match product name and description
            products_searched = ProductClass.objects.order_by(
                                '-created_date').filter(
                                                Q(description__icontains=keyword)|
                                                Q(product_name__icontains=keyword))
            product_count = products_searched.count()

    info_to_render = {
     'products_available':products_searched,
     'product_count':product_count,
    }

    return render(request, 'store/store_file.html', info_to_render)
