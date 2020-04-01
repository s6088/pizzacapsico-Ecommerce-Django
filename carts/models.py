from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from datetime import datetime
import math


from products.models import Product


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
        else:
            cart_obj = self.model.objects.create()
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj



class Cart(models.Model):
    count       = models.PositiveIntegerField(default=0)
    subtotal       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)





class EntryManager(models.Manager):
    def new_or_get(self, cart, product):
        created = False
        qs = self.get_queryset().filter(
                cart = cart, 
                product = product
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    cart = cart, 
                product = product)
            created = True
        return obj, created

    def count(self, cart, product):
        qs = self.get_queryset().filter(
                cart = cart, 
                product = product
            )
        if qs.count() == 1:
            return qs.first().quantity
        return 0


    def get_cart(self, cart):
        return Entry.objects.filter(cart=cart).exclude(quantity=0)




class Entry(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,  on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    objects = EntryManager()

    def __str__(self):
        return "{} {}(s). of cart {}".format(self.quantity, self.product.title, self.cart)



def post_save_entry_receiver(sender, instance, *args, **kwargs):
    entries = Entry.objects.filter(cart=instance.cart)
    subtotal = 0.0
    count = 0
    for x in entries:
        count += x.quantity
        subtotal = math.fsum([x.cost, subtotal])

    instance.cart.subtotal = subtotal
    instance.cart.total = subtotal + ((subtotal*3.5)/100.0)
    instance.cart.count = count
    instance.cart.updated = datetime.now()
    instance.cart.save()


post_save.connect(post_save_entry_receiver, sender=Entry)

def entry_pre_save_receiver(sender, instance, *args, **kwargs):
    x = instance.quantity * instance.product.price
    instance.cost = format(x, '.2f')

pre_save.connect(entry_pre_save_receiver, sender=Entry)