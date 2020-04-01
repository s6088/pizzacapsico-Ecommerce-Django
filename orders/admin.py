from django.contrib import admin

from .models import Order, ProductPurchase, Contact


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'billing_profile' , 'show_location', 'timestamp',)
    search_fields = ('order_id', )
    #exclude = ('slug', )
    list_filter = ('status',)

    # def get_queryset(self, request):
    #    queryset = super(OrderAdmin, self).get_queryset(request).by_status('paid').order_by('-timestamp')
    #    return queryset

    def show_location(self, obj):
        return '<a href="%s">%s</a>' % (obj.location, obj.shipping_address)

    
        
    show_location.allow_tags = True
    show_location.short_description = 'Address & Phone'

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'people', 'time', )

admin.site.register(Order, OrderAdmin)
admin.site.register(Contact, ContactAdmin)


class ProductPurchaseAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'billing_profile', 'product', 'quantity', 'timestamp')
    search_fields = ('order_id',)

admin.site.register(ProductPurchase, ProductPurchaseAdmin)