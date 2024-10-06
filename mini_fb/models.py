from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    image_url = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



