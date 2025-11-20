from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    """
    Project model to manage different projects
    Each project can have multiple members and tasks
    """
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=200, 
        verbose_name='Project Name',
        help_text='Enter a unique project name'
    )
    description = models.TextField(
        verbose_name='Project Description',
        help_text='Detailed description of the project'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='planning',
        verbose_name='Project Status'
    )
    
    # Relationships
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_projects',
        verbose_name='Project Owner',
        help_text='User who created and owns this project'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='projects', 
        blank=True,
        verbose_name='Project Members',
        help_text='Team members working on this project'
    )
    
    # Dates
    start_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Start Date'
    )
    end_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='End Date'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
    
    def get_progress(self):
        """Calculate project completion percentage based on tasks"""
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(status='completed').count()
        return int((completed_tasks / total_tasks) * 100)
    
    def get_total_tasks(self):
        """Get total number of tasks in this project"""
        return self.tasks.count()
    
    def get_completed_tasks(self):
        """Get number of completed tasks"""
        return self.tasks.filter(status='completed').count()
    
    def get_pending_tasks(self):
        """Get number of pending tasks (not completed)"""
        return self.tasks.exclude(status='completed').count()
    
    def is_overdue(self):
        """Check if project has passed its end date"""
        if self.end_date:
            return timezone.now().date() > self.end_date
        return False
    
    def get_members_count(self):
        """Get number of team members"""
        return self.members.count()
    
    def can_user_access(self, user):
        """Check if a user can access this project"""
        return user == self.owner or user in self.members.all()