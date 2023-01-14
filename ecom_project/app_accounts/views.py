from django.shortcuts import render

# Create your views here.
def register_view(request):
    return render(request,'accounts/register.html')

def login_view(request):
    return render(request, 'accounts/login.html')

def logout_view(request):
    return
