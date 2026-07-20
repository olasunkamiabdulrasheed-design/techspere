from django.db import models
from django.conf import settings


class Resource(models.Model):
    TYPE_CHOICES = [
        ("roadmap", "Roadmap"),
        ("ebook", "E-Book"),
        ("template", "Template"),
        ("cheatsheet", "Cheat Sheet"),
        ("guide", "Guide"),
        ("other", "Other"),
    ]

    CATEGORY_CHOICES = [
        ("python", "Python"),
        ("javascript", "JavaScript"),
        ("ai", "AI / Machine Learning"),
        ("cybersecurity", "Cybersecurity"),
        ("webdev", "Web Development"),
        ("mobiledev", "Mobile Development"),
        ("career", "Career Advice"),
        ("design", "Design / UI-UX"),
        ("devops", "DevOps"),
        ("other", "Other"),
    ]

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="other")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    file = models.FileField(upload_to="resources/files/", blank=True, null=True)
    external_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title