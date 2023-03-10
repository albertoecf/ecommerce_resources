from django.shortcuts import render, redirect
from django.http import JsonResponse
from app_carts.models import CartItemClass
from .forms import OrderFormClass
import datetime
from .models import OrderClass, PaymentClass, OrderProductClass
import json
from app_store.models import ProductClass
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.


def payments_view(request):
    body = json.loads(request.body)
    order = OrderClass.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])

    payment = PaymentClass(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_id=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Mover todos los carritos items to la tabla order product
    cart_items = CartItemClass.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProductClass()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItemClass.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProductClass.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        product = ProductClass.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItemClass.objects.filter(user=request.user).delete()

    mail_subject = "Thanks for choosing us"
    body = render_to_string("orders/order_received_email.html", {
        'user': request.user,
        'order': order,
    })

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, body, to=[to_email])
    send_email.send()

    info_to_render = {
    "order_number":order.order_number,
    "transID" : payment.payment_id ,

    }

    return JsonResponse(info_to_render)


def place_order_view(request, total=0, quantity=0):
    print('place order view executed')
    current_user = request.user
    cart_items = CartItemClass.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect("app_store:store_view")

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == "POST":
        form = OrderFormClass(request.POST)
        print('request post')
        if form.is_valid():
            print('form valid')
            data = OrderClass()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.province = form.cleaned_data['province']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            print('record saved')
            # we want to create the id with the datetime from day of order
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = OrderClass.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            dic_to_render = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', dic_to_render)

        else:
            return redirect("checkout_view_path")


def order_completed_view(request):

    order_number  = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print('a')
    try:
        order = OrderClass.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProductClass.objects.filter(order_id=order.id)
        print('b')
        subtotal = 0

        for i in ordered_products:
            subtotal += i.quantity * i.product_price
        print('c')
        payment = PaymentClass.objects.get(payment_id=transID)
        print('cc')
        context_to_render = {
        'order':order,
        'ordered_products':ordered_products,
        'transID':payment.payment_id,
        'payment':payment,
        'subtotal':subtotal,
        }
        print('D')
        return render(request,'orders/order_completed.html', context_to_render)

    except(PaymentClass.DoesNotExist, OrderClass.DoesNotExist):
        return redirect('home_view_path')
