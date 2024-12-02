from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Project(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICE = [
        ('Deleted', 'Deleted'),
        ('Restored', 'Restored')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='Restored')

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ToDo(models.Model) :
    STATUS_CHOICE = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='todos')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.title} - {self.description} - {self.status}"