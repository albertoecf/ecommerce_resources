from django.shortcuts import render
from app_store.models import ProductClass, ReviewRatingClass

def home_view(request):

    products_all = ProductClass.objects.all().filter(is_available=True).order_by('created_date')

    for iterable_product in products_all:
        reviews = ReviewRatingClass.objects.filter(product_id=iterable_product.id, status=True)

    context = {
        'products_all' : products_all,
        'reviews':reviews,
    }

    return render(request, "home.html", context)
