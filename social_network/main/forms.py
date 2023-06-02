from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthencticationForm
from django.contrib.auth.models import User
from django.forms.widgets import *


class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(lable='username', widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nickname'}))

    password1 = forms.CharField(label="password", widget=PasswordInput(
        attrs={"class": "form-control", "placeholder": "Password"}))

    password2 = forms.CharField(label="password confirm", widget=PasswordInput(
        attrs={"class": "form-control", "placeholder": "Confirm password"}))

    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'username', 'email',
                  'phone', 'gender', 'date_of_birth', 'password1', 'password2'}

        widgets = {
            'first_name': TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name"
            }),
            "email": EmailInput(attrs={
                "class": "form-control",
                "placeholder": "email@gmail.com"
            }),
            'last_name': TextInput(attrs={
                "class": "form-control",
                "placeholder": "Middle name"
            }),
            'phone': TextInput(attrs={
                'class': "form-control", 
                'placeholder': 'Phone number'
            }), 
            'gender': Select()
        }
