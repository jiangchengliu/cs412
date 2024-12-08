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
        fields = ['email', 'image_url']