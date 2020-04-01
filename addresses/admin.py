from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('address_line_1', 'address_line_2', 'show_location',)

    def show_location(self, obj):
        return '<a href="http://maps.google.com/maps?q=%s,%s">%s</a>' % (obj.latitude, obj.longitude, "see in map")

        
    show_location.allow_tags = True
    show_location.short_description = 'Google Map'


admin.site.register(Address, AddressAdmin)