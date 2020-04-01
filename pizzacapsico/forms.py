from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import ModelForm
from orders.models import Contact

User = get_user_model()


from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime

class ContactForm(forms.ModelForm):
        class Meta:
                model = Contact
                fields = [
                'name',
                'phone',
                'time',
                'people',
                ]
                widgets = {
                        'name' : forms.TextInput(attrs={"class": "form-control", 
                                "placeholder": "name"}),
                        'phone': forms.TextInput(attrs={"class": "form-control", 
                                "value" : "+32",
                                }),
                        'time' : forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={
                                "class": "form-control", 
                                "placeholder": "dd/MM/yyyy hh:mm"
                        }),
                        'people' :  forms.NumberInput(attrs={"class": "form-control", 
                                }),
                }
                # widgets = {
                # 'name' : forms.TextInput(attrs={"class": "form-control", 
                #                 "placeholder": "name"}),

                # 'phone' : forms.TextInput(attrs={"class": "form-control", 
                #                 "placeholder": "+32..."}),
                
                # 'address_line_2' : forms.TextInput(attrs={"class": "form-control", 
                #                 "placeholder": "address line 2"}),
                # }
#     fullname = forms.CharField(
#             widget=forms.TextInput(
#                     attrs={
#                         "class": "form-control", 
#                         "placeholder": "Your full name"
#                     }
#                     )
#             )
#     email    = forms.EmailField(
#             widget=forms.EmailInput(
#                     attrs={
#                         "class": "form-control", 
#                         "placeholder": "Your email"
#                     }
#                     )
#             )
  
#     date = forms.DateTimeField(
#         input_formats=['%d/%m/%Y %H:%M'], 
#         widget=BootstrapDateTimePickerInput()
#     )


    


    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if not "gmail.com" in email:
    #         raise forms.ValidationError("Email has to be gmail.com")
    #     return email

    # def clean_content(self):
    #     raise forms.ValidationError("Content is wrong.")















