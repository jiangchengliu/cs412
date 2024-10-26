# File: views.py
# Author: Jiang Cheng Liu, 10/05/2024
# Description: functions and classes that handle requests from the client.

from django.shortcuts import render
from .models import Profile, StatusMessage
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import StatusMessageForm
from django.urls import reverse
from django.shortcuts import redirect
from .models import Image

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
    template_name = "mini_fb/create_profile_form.html"


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
    template_name = "mini_fb/create_status_form.html"
    

    def form_valid(self, form):
        """
        Override the form_valid method to associate the status message with the profile.
        """
        # Get the profile object based on the primary key in the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # Set the profile for the status message
        form.instance.profile = profile
        
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image.objects.create(img=f, message=sm)
            image.save()
    
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

class UpdateProfileView(UpdateView):
    """
    View that handles updating a profile.
    """
    model = Profile
    fields = ['email', 'image_url', 'city']
    template_name = "mini_fb/update_profile_form.html"
    
    def get_success_url(self):
        """
        Override the get_success_url method to redirect to the profile page after updating the profile.
        """
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """
        Override the get_context_data method to include the profile object in the context.
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context


class DeleteStatusView(DeleteView):
    """
    View that handles deleting a status message.
    """
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    
    def get_success_url(self):
        """
        Override the get_success_url method to redirect to the profile page after deleting the status message.
        """
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs):
        """
        Override the get_context_data method to include the profile object in the context.
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

class UpdateStatusView(UpdateView):
    """
    View that handles updating a status message.
    """
    model = StatusMessage
    fields = ['status_message']
    template_name = "mini_fb/update_status_form.html"
    
    def get_success_url(self):
        """
        Override the get_success_url method to redirect to the profile page after updating the status message.
        """
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def get_context_data(self, **kwargs):
        """
        Override the get_context_data method to include the profile object in the context.
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

class CreateFriendView(View):
    """
    View that handles creating a friendship between two profiles.
    """
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['pk'])
        other_profile = Profile.objects.get(pk=kwargs['other_pk'])
        profile.add_friend(other_profile)
        return  redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.object.get_friend_suggestions()
        return context

    
from django.views.generic import DetailView
from .models import Profile

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the profile using self.object instead of querying again
        profile = self.object
        
        # Get statuses using the method defined in the Profile model
        statuses = profile.get_news_feed()
        
        # Adding statuses and profile to the context
        context['statuses'] = statuses
        return context
