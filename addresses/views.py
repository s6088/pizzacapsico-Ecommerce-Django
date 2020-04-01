
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from pizzacapsico.utils import getDistanceFromLatLonInKm

from billing.models import BillingProfile
from .forms import AddressCheckoutForm
from .models import Address


def checkout_address_create_view(request):
    form = AddressCheckoutForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request)

        if billing_profile is not None:
            instance.billing_profile = billing_profile
            lat = float(instance.latitude)
            lng = float(instance.longitude)
            dis = getDistanceFromLatLonInKm(lat, lng)
            instance.far = (dis > 2.0)
            instance.save()
            request.session["shipping_address_id"] = instance.id
        else:
            print("Error here")
            return redirect("cart:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("cart:checkout")
