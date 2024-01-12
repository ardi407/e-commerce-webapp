from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields =["address", "city", "state", "zipcode"]