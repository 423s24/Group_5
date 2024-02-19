from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UserAccount
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = UserAccount
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

class AuthForm(AuthenticationForm):
    pass