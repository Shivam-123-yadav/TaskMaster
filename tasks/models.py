from django.db import models
from django.conf import settings
from django.utils import timezone
from projects.models import Project

class Task(models.Model):
    """
    Task model for managing individual tasks within projects
    """
    
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    title = models.CharField(
        max_length=200, 
        verbose_name='Task Title',
        help_text='Brief title for the task'
    )
    description = models.TextField(
        verbose_name='Task Description',
        help_text='Detailed description of what needs to be done'
    )
    
    # Relationships
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name='Project',
        help_text='Project this task belongs to'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tasks',
        verbose_name='Assigned To',
        help_text='User responsible for this task'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_tasks',
        verbose_name='Created By',
        help_text='User who created this task'
    )
    
    # Task Properties
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='todo',
        verbose_name='Status'
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        verbose_name='Priority Level'
    )
    
    # Dates
    due_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Due Date',
        help_text='Deadline for task completion'
    )
    completed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Completed At'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['due_date']),
        ]
    
    def save(self, *args, **kwargs):
        """Override save to set completed_at timestamp"""
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != 'completed':
            self.completed_at = None
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        """Check if task is past its due date"""
        if self.due_date and self.status != 'completed':
            return timezone.now().date() > self.due_date
        return False
    
    def get_comments_count(self):
        """Get number of comments on this task"""
        return self.comments.count()
    
    def get_attachments_count(self):
        """Get number of attachments"""
        return self.attachments.count()
    
    def mark_as_completed(self):
        """Mark task as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def get_priority_color(self):
        """Get color code for priority"""
        colors = {
            'low': 'green',
            'medium': 'yellow',
            'high': 'orange',
            'urgent': 'red'
        }
        return colors.get(self.priority, 'gray')
    
    def get_status_color(self):
        """Get color code for status"""
        colors = {
            'todo': 'gray',
            'in_progress': 'blue',
            'review': 'yellow',
            'completed': 'green',
            'blocked': 'red'
        }
        return colors.get(self.status, 'gray')


class Comment(models.Model):
    """
    Comment model for task discussions and updates
    """
    
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Task',
        help_text='Task this comment belongs to'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='User',
        help_text='User who posted this comment'
    )
    content = models.TextField(
        verbose_name='Comment',
        help_text='Your comment or update'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Posted At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Edited')
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def is_edited(self):
        """Check if comment was edited after creation"""
        return self.updated_at > self.created_at


class Attachment(models.Model):
    """
    Attachment model for uploading files to tasks
    """
    
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='attachments',
        verbose_name='Task',
        help_text='Task this file is attached to'
    )
    file = models.FileField(
        upload_to='task_attachments/%Y/%m/%d/',
        verbose_name='File',
        help_text='Upload a file (max 10MB)'
    )
    file_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='File Name'
    )
    file_size = models.PositiveIntegerField(
        default=0,
        verbose_name='File Size (bytes)'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='uploaded_files',
        verbose_name='Uploaded By'
    )
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At')
    
    def __str__(self):
        return f"Attachment for {self.task.title}"
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'
    
    def save(self, *args, **kwargs):
        """Override save to set file name and size"""
        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    def get_file_size_display(self):
        """Get human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def get_file_extension(self):
        """Get file extension"""
        return self.file_name.split('.')[-1].upper() if '.' in self.file_name else 'FILE'