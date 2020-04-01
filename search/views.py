from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

from carts.models import Cart, Entry

class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        entries = Entry.objects.filter(cart=cart_obj)
        entry_list = {}
        for x in entries:
            entry_list[x.product.id] = x.quantity
        context['quantity'] = entry_list
        context['cart'] = cart_obj

        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) 
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()

