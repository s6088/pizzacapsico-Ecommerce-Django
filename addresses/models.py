from django.db import models
from django.urls import reverse
from billing.models import BillingProfile
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    name            = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True, help_text='Drag the marker to your location')
    postal_code     = models.CharField(max_length=10)
    far = models.BooleanField(default=True, help_text='shipping charge will be added')
    latitude        = models.CharField(default='50.830149', max_length=50, blank=True, null=True)
    longitude       = models.CharField(default='4.385636', max_length=50, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)

    def get_address(self):
        return "{for_name}\n{line1}\n{line2}".format(
                for_name = self.name or "",
                line1 = self.address_line_1,
                line2 = self.address_line_2)
 
    def __str__(self):
        return str(str(self.name) + " | " + str(self.address_line_1) + ", " + str(self.address_line_2) + " | " + str(self.phone))

