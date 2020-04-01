from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .forms import ContactForm
from products.models import Product, Category
from carts.models import Cart, Entry
from django.conf import settings
from google.cloud import storage


def home_page(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    entries = Entry.objects.filter(cart=cart_obj)
    entries2 = {}
    for x in entries:
        entries2[x.product.id] = x
    products = []
    category = Category.objects.all().order_by('-priority')
    for cat in category:
        products.append(Product.objects.filter(category=cat, available=True))
    return render(request, "home_page.html", { 'category' : category, 'products' : products, 'entries' : entries2})

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Reservation",
        "content":"Welcome to Capsico",
        "form": contact_form,
    }

    if contact_form.is_valid():
        contact = contact_form.save(commit=False)
        contact.save()
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your reservation"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
            
    return render(request, "contact/view.html", context)


def about_page(request):
    return render(request, "about.html", {})