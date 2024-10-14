# File: views.py
# Author: Jiang Cheng Liu, 10/05/2024
# Description: functions and classes that handle requests from the client.

from django.shortcuts import render
from .models import Profile, StatusMessage
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .forms import StatusMessageForm
from django.urls import reverse

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

class ShowProfilePageView(DetailView):
    """
    View that returns a single profile page.
    Inherits from Django's DetailView, which provides a page
    displaying a single object.
    """
    
    # The model that this view will retrieve data from (Profile model).
    model = Profile
    # The template that will be rendered for this view.
    template_name = "mini_fb/show_profile.html"
    # Override the get_context_data method to include custom data in the context
    def get_context_data(self, **kwargs):
        # Get the default context data (which includes the profile object)
        context = super().get_context_data(**kwargs)
        
        # Call the accessor method from the Profile object (self.object)
        context['status_messages'] = self.object.get_status_messages()
        
        return context

class CreateProfileView(CreateView):
    """
    View that handles creating a new profile.
    Inherits from Django's CreateView, which provides a form
    for creating a new object.
    """
    
    # The model that this view will create objects for (Profile model).
    model = Profile
    # The fields that will be displayed in the form for creating a new profile.
    fields = ['first_name', 'last_name', 'email', 'image_url', 'city']
    # The template that will be rendered for this view.
    template_name = "mini_fb/create_profile.html"


class CreateStatusView(CreateView):
    """
    View that handles creating a new status message.
    Inherits from Django's CreateView, which provides a form
    for creating a new object.
    """
    
    # The model that this view will create objects for (StatusMessage model).
    model = StatusMessage
    # The fields that will be displayed in the form for creating a new status message.
    fields = ['status_message']
    # The template that will be rendered for this view.
    template_name = "mini_fb/create_status.html"
    

    def form_valid(self, form):
        """
        Override the form_valid method to associate the status message with the profile.
        """
        # Get the profile object based on the primary key in the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # Set the profile for the status message
        form.instance.profile = profile
        # Call the parent class' form_valid method to save the form
        return super().form_valid(form)

    def get_success_url(self):
        """
        Override the get_success_url method to redirect to the profile page after creating a status message.
        """
        # Get the profile object based on the primary key in the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])
       
        return reverse('show_profile', kwargs={'pk': profile.pk})

    def get_context_data(self, **kwargs):
        """
        Override the get_context_data method to include the profile object in the context.
        """
        # Get the default context data
        context = super().get_context_data(**kwargs)
        # Get the profile object based on the primary key in the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # Add the profile object to the context
        context['profile'] = profile
        return context

        


