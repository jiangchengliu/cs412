from django.db import models
from django.urls import reverse
from django.db.models import Q

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
    
    def get_friends(self):
        """
        Return all friends for this profile
        """
        friends = Friend.objects.filter(Q(profile1=self) | Q(profile2=self))
        
        # Extract the friend profiles (i.e., the profile that is not 'self')
        friends_profiles = [
            friend.profile2 if friend.profile1 == self else friend.profile1
            for friend in friends
        ]
        
        return friends_profiles
    
    def add_friend(self, other):
        # Prevent self-friending
        if self == other:
            return
        
        # Check if friendship already exists
        friendship_exists = Friend.objects.filter(
            (Q(profile1=self) & Q(profile2=other)) | (Q(profile1=other) & Q(profile2=self))
        ).exists()
        
        # If no friendship exists, create a new Friend instance
        if not friendship_exists:
            Friend.objects.create(profile1=self, profile2=other)
    
    def get_friend_suggestions(self):
        '''Returns friend suggestions for this profile'''
        friends = self.get_friends()
        friends.append(self)
        suggestions = Profile.objects.exclude(id__in=[f.id for f in friends])
        return suggestions
    
    def get_news_feed(self):
        '''Returns the news feed for this profile'''
        friends = self.get_friends()
        messages = StatusMessage.objects.filter(profile__in=friends).order_by('-created_at')
        return list(messages)


class StatusMessage(models.Model):
    """
    Created a StatusMessage model with the following information
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.first_name}'s status message"
    
    def get_images(self):
        """
        Return all images for this status message
        """
        return Image.objects.filter(message=self)

class Image(models.Model):
    """
    Created an Image model with the following information
    """
    img = models.ImageField()
    message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    uploaded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.message.profile.first_name}"

class Friend(models.Model):
    """
    Created a Friend model with the following information
    """
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name}  is friends with {self.profile2.first_name} {self.profile2.last_name}"
    
    def get_absolute_url(self):
        return reverse("show_profile", kwargs={"pk": self.profile.pk})

