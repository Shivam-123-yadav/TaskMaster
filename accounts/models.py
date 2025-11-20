from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Adds additional fields like role, bio, avatar, phone
    """
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Team Member'),
    ]
    
    # Override email to make it unique and required
    email = models.EmailField(unique=True, verbose_name='Email Address')
    
    # Additional fields
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='member',
        verbose_name='User Role'
    )
    bio = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Biography',
        help_text='Tell us about yourself'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name='Profile Picture'
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='Phone Number'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Joined Date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name_or_username(self):
        """Return full name if available, otherwise username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'
    
    def is_manager(self):
        """Check if user has manager role"""
        return self.role == 'manager'
    
    def get_assigned_tasks_count(self):
        """Get count of tasks assigned to this user"""
        return self.assigned_tasks.count()
    
    def get_created_projects_count(self):
        """Get count of projects owned by this user"""
        return self.owned_projects.count()