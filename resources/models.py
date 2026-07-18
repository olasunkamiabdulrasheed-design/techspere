from django.db import models
from django.conf import settings


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ("roadmap", "Roadmap"),
        ("ebook", "E-Book"),
        ("template", "Template"),
        ("cheatsheet", "Cheat Sheet"),
        ("guide", "Guide"),
        ("other", "Other"),
    ]

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    file = models.FileField(upload_to="resources/", blank=True, null=True)
    external_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
