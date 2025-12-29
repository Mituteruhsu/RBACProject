from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from logs.models import ActivityLog


class Command(BaseCommand):
    help = "Delete old activity logs"

    def handle(self, *args, **options):
        days = getattr(settings, 'ACTIVITY_LOG_RETENTION_DAYS', 90)
        cutoff = timezone.now() - timedelta(days=days)

        deleted, _ = ActivityLog.objects.filter(
            created_at__lt=cutoff
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(f"Deleted {deleted} activity logs")
        )
