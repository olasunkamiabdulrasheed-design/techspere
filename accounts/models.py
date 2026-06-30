from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, help_text="Comma-separated skills")
    experience_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='beginner'
    )
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    portfolio_link = models.URLField(blank=True)

    def __str__(self):
        return self.username

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]