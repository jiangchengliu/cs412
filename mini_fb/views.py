# File: views.py
# Author: Jiang Cheng Liu, 10/05/2024
# Description: functions and classes that handle requests from the client.

from django.shortcuts import render
from .models import Profile
from django.http import HttpResponse
from django.views.generic import ListView

# Create your views here.

class ShowAllProfiles(ListView):
    """
    View that returns all profiles in the database.
    Inherits from Django's ListView, which provides a page
    displaying a list of objects.
    """
    
    # The model that this view will retrieve data from (Profile model).
    model = Profile
    # The template that will be rendered for this view.
    template_name = "mini_fb/show_all_profiles.html"
    # The context variable name that will be used in the template
    # to refer to the list of profiles.
    context_object_name = "profiles"
    
    def get_queryset(self):
        """
        Returns the queryset of all Profile objects in the database.
        This can be customized to filter or modify the profiles displayed.
        """
        return Profile.objects.all()





