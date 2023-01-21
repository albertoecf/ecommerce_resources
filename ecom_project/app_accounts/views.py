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
from app_carts.views import _cart_id
from app_carts.models import CartClass, CartItemClass
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
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Get started with Ceibo"
            body = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email_from_form
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email=' + email_from_form)

    context_to_render = {'form': form}

    return render(request, 'accounts/register.html', context_to_render)


def login_view(request):
    if request.method == 'POST':
        email_user_input = request.POST['email']
        password_user_input = request.POST['password']

        user = auth.authenticate(
            email=email_user_input, password=password_user_input)

        if user is not None:
            print("user is not none")
            try:
                print("try accessedd")
                cart = CartClass.objects.get(cart_id = _cart_id(request))
                print("Cart initiated")
                is_cart_item_exists = CartItemClass.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    print('cart_items_exist : ')
                    cart_item = CartItemClass.objects.filter(cart=cart)

                    prouct_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    cart_item = CartItemClass.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItemClass.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItemClass.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                print("did not match the cart with the user")
                pass

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


def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = AccountClass._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, AccountClass.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congrats, your account is active")
        return redirect("app_accounts:login_view_path")
    else:
        messages.error(request, "Please try registering again")
        return redirect("app_accounts:register_view_path")


@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


def forgot_password_view(request):
    if request.method == 'POST':
        email_from_request = request.POST.get('email')
        if AccountClass.objects.filter(email=email_from_request).exists():
            user = AccountClass.objects.get(email__exact=email_from_request)

            current_site = get_current_site(request)
            mail_subject = "Reset your Password"
            body = render_to_string("accounts/reset_password_email.html", {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email_from_request
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            messages.success(
                request, "Please check your email, we sent you a link to reset your password")

            return redirect("app_accounts:login_view_path")

        else:
            messages.error(request, "Email does not exist")
            return redirect("app_accounts:forgot_password_view_path")

    return render(request, "accounts/forgotPassword.html")


def reset_password_validate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = AccountClass._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, AccountClass.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please, reset your password')
        return redirect("app_accounts:reset_password_view_path")
    else:
        messages.error(request, "Link has expired")
        return redirect("app_accounts:login_view_path")


def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = AccountClass.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset correctly')
            return redirect('app_accounts:login_view_path')

        else:
            messages.error(request, "Password confirmation does not match")
            return redirect("app_accounts:reset_password_view_path")
    else:
        return render(request, "accounts/reset_password.html")
