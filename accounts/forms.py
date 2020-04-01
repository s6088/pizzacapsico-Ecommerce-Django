from django import forms

from .models import GuestEmail


class GuestForm(forms.ModelForm):
    email    = forms.EmailField(
            widget=forms.EmailInput(
                    attrs={
                        "label" : "Enter Your Email",
                        "class": "form-control", 
                        "placeholder": "example@gmail.com"
                    }
                    )
            )
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
            request.session['guest_email'] = obj.email
        return obj

