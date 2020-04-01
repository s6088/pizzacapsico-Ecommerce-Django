from django.urls import re_path

from .views import list_view
app_name = 'products'
urlpatterns = [
    re_path(r'^$', list_view, name='list'),
]
