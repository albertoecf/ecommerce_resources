from django.shortcuts import render
from app_store.models import ProductClass

def home_view(request):

    products_all = ProductClass.objects.all().filter(is_available=True)

    context = {
        'products_all' : products_all
    }

    return render(request, "home.html", context)
