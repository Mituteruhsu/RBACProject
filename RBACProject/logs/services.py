# logs/services.py
from django.conf import settings
from .tasks import create_activity_log
from .models import ActivityLog

def log_activity(**data):
    if getattr(settings, 'ACTIVITY_LOG_ASYNC', False):
        create_activity_log.delay(**data)
    else:
        ActivityLog.objects.create(**data)
