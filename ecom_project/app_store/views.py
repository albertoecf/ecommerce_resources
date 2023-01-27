from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .models import ProductClass, ReviewRatingClass
from app_category.models import CategoryClass
from app_carts.models import CartItemClass
from app_carts.views import _cart_id
from .forms import ReviewFormClass
from django.contrib import messages

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
    products_searched = ProductClass.objects.order_by('-created_date')
    product_count = products_searched.count()
    #are we receiving a keyword in the request?
    if 'keyword' in request.GET :
        keyword = request.GET['keyword'].strip()
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

def submit_review_view(request, product_id):
    print('submit view excecuted')
    request_url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRatingClass.objects.get(user__id = request.user.id, product__id=product_id)
            form = ReviewFormClass(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thanks for rating")
            print('s')
            return redirect(request_url)
        except ReviewRatingClass.DoesNotExist:
            form = ReviewFormClass(request.POST)
            if form.is_valid():
                data = ReviewRatingClass()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id  = request.user.id
                data.save()
                print('sa')
                messages.success(request, "Thanks for rating")
                return redirect(request_url)
