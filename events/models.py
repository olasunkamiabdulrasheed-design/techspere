from django.db import models
from django.conf import settings


class Event(models.Model):
    EVENT_TYPES = [
        ('hackathon', 'Hackathon'),
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('meetup', 'Meetup'),
        ('competition', 'Competition'),
    ]

    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events_organized')
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='meetup')
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, help_text="Physical location or 'Online'")
    event_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(null=True, blank=True)
    max_participants = models.IntegerField(null=True, blank=True)
    prize = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title

    @property
    def participant_count(self):
        return self.registrations.count()

    @property
    def is_full(self):
        if not self.max_participants:
            return False
        return self.participant_count >= self.max_participants


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'participant']

    def __str__(self):
        return f"{self.participant} → {self.event}"