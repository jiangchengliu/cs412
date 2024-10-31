# File: views.py
# Author: Jiang Cheng Liu, 10/05/2024
# Description: functions and classes that handle requests from the client.

from django.shortcuts import render
from .models import Profile, StatusMessage
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from .forms import StatusMessageForm
from .forms import CreateProfileForm 
from django.urls import reverse_lazy, reverse
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
    
    def get_object(self):
        """
        Returns the Profile object that the view is displaying.
        This can be customized to retrieve a specific profile.
        """
        # Get the primary key of the profile fr
        return Profile.objects.get(user=self.request.user)
    
    # Override the get_context_data method to include custom data in the context
    def get_context_data(self, **kwargs):
        # Get the default context data (which includes the profile object)
        context = super().get_context_data(**kwargs)
        
        # Call the accessor method from the Profile object (self.object)
        context['status_messages'] = self.object.get_status_messages()
        
        return context

    def get_login_url(self):
        return reverse_lazy('mini_fb/login')

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    
    def success_url(self):
        return reverse('login')

    def get_context_data(self, **kwargs):
        # Call the superclass method first to get the context
        context = super().get_context_data(**kwargs)
        # Create an instance of UserCreationForm and add it to the context
        context['user_creation_form'] = UserCreationForm()
        return context
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Get the user creation form data
        user_creation_form = UserCreationForm(self.request.POST)

        if user_creation_form.is_valid():
            # Save the user instance and attach it to the profile
            user = user_creation_form.save()
            profile = form.instance
            profile.user = user  
            profile.save()  
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_creation_form=user_creation_form))


class CreateStatusView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    fields = ['status_message']
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
        profile = self.get_object()  
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(img=f, message=sm)
        return super().form_valid(form)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()  # Pass profile to context
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View that handles updating a profile.
    """
    model = Profile
    fields = ['email', 'image_url', 'city']
    template_name = "mini_fb/update_profile_form.html"
    
    def get_object(self):
        """
        Override the get_object method to return the profile of the currently logged in user.
        """
        return Profile.objects.get(user=self.request.user)
    
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


class DeleteStatusView(LoginRequiredMixin, DeleteView):
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

class UpdateStatusView(LoginRequiredMixin, UpdateView):
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

class CreateFriendView(LoginRequiredMixin, View):
    """
    View that handles creating a friendship between two profiles.
    """

    def get_object(self):
        # Get the profile of the logged-in user
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        # Get the profile of the logged-in user
        profile = self.get_object()
        
        # Get the other profile using the 'other_pk' parameter from the URL
        other_profile = Profile.objects.get(pk=kwargs['other_pk'])
        
        # Add the other profile as a friend
        profile.add_friend(other_profile)
        
        # Redirect to the show profile page of the logged-in user
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.object.get_friend_suggestions()
        return context


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the profile using self.object instead of querying again
        profile = self.object
        
        # Get statuses using the method defined in the Profile model
        statuses = profile.get_news_feed()
        
        # Adding statuses and profile to the context
        context['statuses'] = statuses
        return context
