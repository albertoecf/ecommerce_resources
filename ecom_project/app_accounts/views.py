from django.shortcuts import render
from .forms import RegistrationFormClass
# Create your views here.
def register_view(request):
    form =  RegistrationFormClass()

    context_to_render = {'form':form}

    return render(request,'accounts/register.html', context_to_render )

def login_view(request):
    return render(request, 'accounts/login.html')

def logout_view(request):
    return
