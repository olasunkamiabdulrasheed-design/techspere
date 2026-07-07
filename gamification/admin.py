from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserXP, XPLog, Badge, UserBadge

admin.site.register(UserXP)
admin.site.register(XPLog)
admin.site.register(Badge)
admin.site.register(UserBadge)
