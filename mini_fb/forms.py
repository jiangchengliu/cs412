from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """
    Form for creating a new profile.
    """
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'image_url', 'city']
    

class StatusMessageForm(forms.ModelForm):
    """
    Form for creating a new status message.
    """
    class Meta:
        model = StatusMessage
        fields = ['status_message']