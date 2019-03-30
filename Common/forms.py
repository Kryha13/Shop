from django.contrib.auth.forms import UserCreationForm

from Shop.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username',  'password1', 'password2']
