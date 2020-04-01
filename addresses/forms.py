from django import forms

from .models import Address

#shipping address


class AddressCheckoutForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            'name',
            'phone',
            'address_line_1',
            'address_line_2',
            'longitude',
            'latitude',
        ]
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control",
                                           "placeholder": "full name"}),

            'phone': forms.TextInput(attrs={"class": "form-control",
                                            "value": "+32"
                                            }),

            'address_line_1': forms.TextInput(attrs={"class": "form-control",
                                                     "id": "pac-input",
                                                     "placeholder": "address line 1"}),

            'address_line_2': forms.TextInput(attrs={"class": "form-control",
                                                     "placeholder": "address line 2"}),

            'longitude': forms.TextInput(attrs={
                "type": "hidden",
                "id": "longitude",
            }),

            'latitude': forms.TextInput(attrs={
                "type": "hidden",
                "id": "latitude",
            }),
        }
