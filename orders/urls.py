from django.urls import re_path

from .views import (
        OrderListView, 
        OrderDetailView,
        VerifyOwnership
        )

urlpatterns = [
    re_path(r'^$', OrderListView.as_view(), name='list'),
    re_path(r'^endpoint/verify/ownership/$', VerifyOwnership.as_view(), name='verify-ownership'),
    re_path(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDetailView.as_view(), name='detail'),
]