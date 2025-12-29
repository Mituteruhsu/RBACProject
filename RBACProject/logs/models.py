from django.db import models
from django.conf import settings
from .querysets import ActivityLogQuerySet

class ActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=255, default='UNKNOWN')
    method = models.CharField(max_length=10, default='UNKNOWN')
    action = models.CharField(max_length=100, default='UNKNOWN')
    extra = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = ActivityLogQuerySet.as_manager()
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.user.username} - {self.action}'
