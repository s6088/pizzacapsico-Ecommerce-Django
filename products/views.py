from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect


from .models import Product, Category
from carts.models import Cart, Entry


def menu_page(request):
    products = []
    category = Category.objects.all().order_by('-priority')
    for cat in category:
        products.append(Product.objects.filter(category=cat, available=True))
    return render(request, "products/mlist.html", {'products': products})


def list_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    entries = Entry.objects.filter(cart=cart_obj)
    entries2 = {}
    for x in entries:
        entries2[x.product.id] = x
    products = []
    category = Category.objects.all().order_by('-priority')
    for cat in category:
        products.append(Product.objects.filter(category=cat, available=True))
    return render(request, "products/olist.html", { "products" : products, "entries" : entries2 })
