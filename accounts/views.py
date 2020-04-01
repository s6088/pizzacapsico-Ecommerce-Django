
from django.views.generic import CreateView
from django.shortcuts import redirect

from .forms import GuestForm

from pizzacapsico.mixins import NextUrlMixin, RequestFormAttachMixin


class GuestRegisterView(NextUrlMixin,  RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)
