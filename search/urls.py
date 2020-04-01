from django.urls import re_path

from .views import SearchProductView
        
app_name = 'search'
urlpatterns = [
    re_path(r'^$', SearchProductView.as_view(), name='query'),
]

