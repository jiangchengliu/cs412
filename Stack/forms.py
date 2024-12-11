# File: models.py
# Author: Jiang Cheng Liu (jiangcl@bu.edu)
# Date: 12/10/2024
# Description: django forms utilized in the views, used to create and update user profiles.


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import * 


from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, help_text="Required")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        required=True,
        help_text="Enter your password"
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'image_url']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'image_url', 'balance']