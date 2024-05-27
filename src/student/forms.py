from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateNewUser(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    birth_day = forms.DateField(required=True)
    university = forms.CharField(max_length=100 , required=True)
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "email",
        ]
