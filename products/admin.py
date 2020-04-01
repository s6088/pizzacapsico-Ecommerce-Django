from django.contrib import admin
from .models import Product, Category



class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'available', 'price')
    exclude = ('slug', )
    list_filter = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority')
    list_filter = ('priority',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)


admin.site.site_header = 'Capsico Dashboard'



