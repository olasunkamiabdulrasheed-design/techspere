from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPES = [
        ('comment', 'Comment on your post'),
        ('join_request', 'Someone applied to your project'),
        ('accepted', 'Your application was accepted'),
        ('rejected', 'Your application was rejected'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.notification_type}"