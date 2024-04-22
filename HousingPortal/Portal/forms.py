from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UserAccount, Building
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = UserAccount
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]
        help_texts = {
            'username': 'Required. 30 characters or fewer. Only lowercase letters, numbers, hyphen, underscore, and period are allowed.',
        }

class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        # Override the default error message
        self.error_messages['invalid_login'] = (
            "Invalid username or password."
        )
        
    def clean_username(self):
        username = self.cleaned_data['username']
        # Transform the username to lowercase
        return username.lower()

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ["building_name", "address", "city", "state", "country", "zipcode"]