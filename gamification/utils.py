from .models import UserXP, XPLog

XP_VALUES = {
    'signup': 10,
    'post': 15,
    'comment': 5,
    'project': 20,
    'apply': 10,
    'job': 20,
}

DESCRIPTIONS = {
    'signup': 'Joined TechSphere',
    'post': 'Created a post',
    'comment': 'Left a comment',
    'project': 'Posted a project',
    'apply': 'Applied to a project',
    'job': 'Posted a job',
}

def award_xp(user, action):
    points = XP_VALUES.get(action, 0)
    if not points:
        return

    xp, created = UserXP.objects.get_or_create(user=user)
    xp.total_xp += points
    xp.save()

    XPLog.objects.create(
        user=user,
        action=action,
        points=points,
        description=DESCRIPTIONS.get(action, action)
    )