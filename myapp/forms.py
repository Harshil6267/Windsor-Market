from django import forms
from django.db import models
from myapp.models import *
from django.contrib.auth.forms import UserCreationForm


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']

    client = forms.ModelChoiceField(queryset=Client.objects.all(), label='Client Name')
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    num_units = forms.IntegerField(label='Quantity')


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1,'Interested'),(0,'Not interested')], label='Intrested')
    quantity = forms.IntegerField(initial=1, label='Quantity')
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Comments')


class Register(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Client
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'city', 'province', 'interested_in', 'profile_image')


# class LoginForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput)
#     password = forms.CharField(widget=forms.PasswordInput)
