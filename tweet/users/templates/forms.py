from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from ..models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'form-control',
    }))

    user_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter a username',
        'class': 'form-control',
    }))

    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'placeholder': 'yyyy-mm-dd (DOB)',
        'class': 'form-control',
        'type': 'date',
    }))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter a password',
        'class': 'form-control',
    }))

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Re-type password',
        'class': 'form-control',
    }))

    class Meta:
        model = CustomUser
        fields = ("email", "user_name", "date_of_birth", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "user_name",)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Email/ Username',
        'class': 'form-control'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))

