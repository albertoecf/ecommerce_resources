from django.shortcuts import render
from .models import ProductClass

# Create your views here.
def store_view(request):
    products_available = ProductClass.objects.all().filter(is_available=True)
    product_count  = products_available.count()

    info_to_render = {
        'products_available' : products_available,
        'product_count' : product_count
    }
    return render(request,'store/store_file.html', info_to_render)
