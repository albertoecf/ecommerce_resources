from django.shortcuts import render,redirect
from .forms import RegistrationFormClass
from .models import AccountClass
from django.contrib import messages, auth

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
            messages.success(request, 'User created')
            return redirect('app_accounts:register_view_path')
    context_to_render={'form': form}

    return render(request, 'accounts/register.html', context_to_render)


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user  = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home_view_path")
        else :
            messages.error(request, "Invalid credentials")
            return redirect("app_accounts:login_view_path")

    return render(request, 'accounts/login.html')


def logout_view(request):
    return
