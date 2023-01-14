from django.shortcuts import render
from .forms import RegistrationFormClass
from .models import AccountClass

# Create your views here.


def register_view(request):
    form = RegistrationFormClass()
    if request.method == "POST":
        form = RegistrationFormClass(request.POST)
        if form.is_valid():
            first_name_from_form = form.cleaned_data['first_name']
            last_name_from_form = form.cleaned_data['last_name']
            email_from_form = form.cleaned_data['email']
            password_from_form = form.cleaned_data['password']
            username_from_form = email_from_form.split("@")[0]
            user = AccountClass.objects.create_user(
                first_name=first_name_from_form,
                last_name=last_name_from_form,
                username = username_from_form, 
                email=email_from_form,
                password=password_from_form)
            user.save()

    context_to_render={'form': form}

    return render(request, 'accounts/register.html', context_to_render)


def login_view(request):
    return render(request, 'accounts/login.html')


def logout_view(request):
    return
