from django.shortcuts import render

# Create your views here.
def cart_view(request):
    return render(request, 'store/cart.html')
