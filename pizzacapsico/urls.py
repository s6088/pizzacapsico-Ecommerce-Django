from django.urls import re_path, path, include
from django.contrib import admin


from .views import home_page, contact_page, about_page
from accounts.views import GuestRegisterView
from addresses.views import checkout_address_create_view
from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_detail_api_view, change_view
from products.views import menu_page

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^$', home_page, name='home'),
    re_path(r'^about/$', about_page, name='about'),
    re_path(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    re_path(r'^contact/$', contact_page, name='contact'),
    re_path(r'^menu/$', menu_page, name='menu'),
    re_path(r'^change/$', change_view, name='change'),
    re_path(r'^checkout/address/create/$', checkout_address_create_view,
        name='checkout_address_create'),
    re_path(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
    re_path(r'^cart/', include("carts.urls",namespace='cart')),
    re_path(r'^billing/payment-method/$', payment_method_view,
        name='billing-payment-method'),
    re_path(r'^billing/payment-method/create/$', payment_method_createview,
        name='billing-payment-method-endpoint'),
    re_path(r'^products/', include("products.urls",namespace='product')),
    re_path(r'^search/', include("search.urls",namespace='search')),
    re_path(r'^towaha/', admin.site.urls),
]

# if settings.DEBUG:
#     urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)