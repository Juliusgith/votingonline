from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidate_photos/')
    details = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Voter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username