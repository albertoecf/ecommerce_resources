from django.shortcuts import render

# Create your views here.
def store_view(request):
    return render(request,'store/store_file.html')
