from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Project(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects_created')
    title = models.CharField(max_length=255)
    description = models.TextField()
    roles_needed = models.CharField(max_length=255, help_text="Comma-separated, e.g. Frontend Developer, UI Designer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JoinRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='join_requests')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant} → {self.project}"