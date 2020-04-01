from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

from django.core.mail import send_mail
from accounts.forms import GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressCheckoutForm
from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order, ProductPurchase
from products.models import Product
from .models import Cart, Entry

import math

MINIMUM_PURCHASE = 5.0


import stripe
STRIPE_SECRET_KEY = getattr(
    settings, "STRIPE_SECRET_KEY", "sk_test_cu1lQmcg1OLffhLvYrSCp5XE")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY",
                         'pk_test_PrV61avxnHaWIYZEeiYTTVMZ')
stripe.api_key = STRIPE_SECRET_KEY


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_data = {
        "subtotal": cart_obj.subtotal,
        "total": cart_obj.total
    }
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if new_obj or cart_obj.subtotal < MINIMUM_PURCHASE:
        return redirect("products:list")
    entries = Entry.objects.get_cart(cart_obj)
    return render(request, "carts/home.html", {"entries": entries, "cart": cart_obj})

def change_view(request):
    del request.session["guest_email_id"]
    return redirect("cart:home")

def cart_update(request):
    product_id = request.POST.get('product_id')
    req = request.POST.get('type')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")
        cart_obj, new_cart = Cart.objects.new_or_get(request)
        entry_obj, new_entry = Entry.objects.new_or_get(cart_obj, product_obj)
        cnt = entry_obj.quantity
        added = 0

        status = "Greetings From Capsico"

        if req == 'inc':
            entry_obj.quantity = cnt+1
            entry_obj.save()
            added = 1
            status = "Item has been added"
        elif req == 'dec' and cnt > 0:
            entry_obj.quantity = cnt-1
            entry_obj.save()
            added = -1
            status = "Item has been removed"
        else:
            return redirect("cart:home")

        cart_obj, new_cart = Cart.objects.new_or_get(request)

        request.session['cart_items'] = cart_obj.count

        if request.is_ajax():
             json_data = {
                 "added": added,
                 "pslug": product_obj.slug,
                 "ptitle": product_obj.title,
                 "equantity": entry_obj.quantity,
                 "ecost": entry_obj.cost,
                 "pprice": product_obj.price,
                 "ccount": cart_obj.count,
             }
             return JsonResponse(json_data, status=200)
    return redirect("cart:home")


def checkout_home(request):

    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.subtotal < MINIMUM_PURCHASE:
        return redirect("products:list")  
    entries = Entry.objects.get_cart(cart_obj)


    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()

    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
        
    has_card = False



    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart_obj)
        request.session['order_obj_id'] = order_obj.id

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            if order_obj.shipping_address.far:
                order_obj.shipping_total = 5.0
            else :
                order_obj.total = math.fsum([order_obj.total, - 5.0])
                order_obj.shipping_total = 0.0
            
            order_obj.save()
            del request.session["shipping_address_id"]

        has_card = billing_profile.has_card

    if request.method == "POST":
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                del request.session['guest_email_id']
                request.session['cart_items'] = 0
                del request.session['cart_id']
                billing_profile.set_cards_inactive()
                txt_ = None
                html_ = get_template("email.html").render({'entries': Entry.objects.filter(cart=order_obj.cart, quantity__gte=1), 'order' : order_obj, 'address' : order_obj.shipping_address})
                subject = 'Order Confirmation From Capsico Order ID ' + order_obj.order_id
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [billing_profile.email]
                send_mail('Order Confirm', 'Thanks For Purchaseing from Capsico', settings.EMAIL_HOST_USER,
                              recipient_list,  html_message=html_, fail_silently=False)

                return redirect("cart:success")
            else:
                return redirect("cart:checkout")
    context = {
        "object": order_obj,
        "entries": entries,
        "billing_profile": billing_profile,
        "guest_form": guest_form,
        "address_form": address_form,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
       

    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
