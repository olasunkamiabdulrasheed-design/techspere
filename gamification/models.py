from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class UserXP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp')
    total_xp = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.total_xp} XP"

    @property
    def rank(self):
        xp = self.total_xp
        if xp >= 5000: return 'Legend'
        if xp >= 2000: return 'Mentor'
        if xp >= 1000: return 'Expert'
        if xp >= 500:  return 'Innovator'
        if xp >= 200:  return 'Builder'
        if xp >= 50:   return 'Explorer'
        return 'Newbie'

    @property
    def rank_color(self):
        rank = self.rank
        colors = {
            'Legend': 'badge-yellow',
            'Mentor': 'badge-purple',
            'Expert': 'badge-blue',
            'Innovator': 'badge-blue',
            'Builder': 'badge-green',
            'Explorer': 'badge-green',
            'Newbie': 'badge-blue',
        }
        return colors.get(rank, 'badge-blue')


class XPLog(models.Model):
    ACTIONS = [
        ('post', 'Created a post', ),
        ('comment', 'Left a comment'),
        ('project', 'Posted a project'),
        ('apply', 'Applied to a project'),
        ('job', 'Posted a job'),
        ('signup', 'Joined TechSphere'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_logs')
    action = models.CharField(max_length=20)
    points = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} +{self.points} XP ({self.action})"


class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=10, default='🏆')

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']