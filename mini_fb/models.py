from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    """
    Created a Profile model with the following information
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    image_url = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        """
        Return the full name of the profile
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        """
        Return all status messages for this profile
        """
        return self.statusmessage_set.all().order_by('-created_at')

    def get_absolute_url(self):
        return reverse("show_profile", kwargs={"pk": self.pk})
    

class StatusMessage(models.Model):
    """
    Created a StatusMessage model with the following information
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.first_name}'s status message"



