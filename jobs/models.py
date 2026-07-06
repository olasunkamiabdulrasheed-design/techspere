from django.db import models
from django.conf import settings


class Job(models.Model):
    JOB_TYPES = [
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
        ('remote', 'Remote'),
    ]

    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs_posted')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='fulltime')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    apply_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('rejected', 'Rejected')],
        default='pending'
    )

    class Meta:
        unique_together = ['job', 'applicant']

    def __str__(self):
        return f"{self.applicant} → {self.job}"