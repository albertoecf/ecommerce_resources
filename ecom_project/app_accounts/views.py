from django.shortcuts import render, redirect
from .forms import RegistrationFormClass
from .models import AccountClass
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
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
                username=username_from_form,
                email=email_from_form,
                password=password_from_form)

            current_site = get_current_site(request)
            mail_subject = "Get started with Ceibo"
            body = render_to_string('account/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_enconde(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            user.save()
            messages.success(request, 'User created')
            return redirect('app_accounts:register_view_path')
    context_to_render = {'form': form}

    return render(request, 'accounts/register.html', context_to_render)


def login_view(request):
    if request.method == 'POST':
        email_user_input = request.POST['email']
        password_user_input = request.POST['password']

        user = auth.authenticate(
            email=email_user_input, password=password_user_input)

        if user is not None:
            auth.login(request, user)
            return redirect("home_view_path")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("app_accounts:login_view_path")

    return render(request, 'accounts/login.html')


@login_required(login_url='login_view_path')
def logout_view(request):
    auth.logout(request)
    messages.success(request, "See you soon!")
    return redirect('app_accounts:login_view_path')
