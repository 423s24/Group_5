from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserAccount

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['email', 'password']

class CustomAuthenticationForm(AuthenticationForm):
    pass