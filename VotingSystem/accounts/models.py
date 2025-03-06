# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
import random
import string

class User(AbstractUser):
    registration_number = models.CharField(max_length=20, unique=True)
    faculty = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    
    # Override the groups field to add a custom related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_set',  # Custom related_name
        related_query_name='accounts_user'
    )
    
    # Override the user_permissions field to add a custom related_name
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_set',  # Custom related_name
        related_query_name='accounts_user'
    )
    
    def __str__(self):
        return self.username

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Code for {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a random 6-digit code
            self.code = ''.join(random.choices(string.digits, k=6))
        
        if not self.expires_at:
            # Set expiry to 30 minutes from now
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30)
            
        super().save(*args, **kwargs)
    
    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at