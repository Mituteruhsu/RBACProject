# logs/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import ActivityLog

User = get_user_model()

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def create_activity_log(self, **data):
    user_id = data.pop('user_id', None)

    if user_id:
        try:
            data['user'] = User.objects.get(id=user_id)
        except User.DoesNotExist:
            data['user'] = None
    else:
        data['user'] = None

    ActivityLog.objects.create(**data)
