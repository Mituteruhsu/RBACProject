from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import require_capability
from .models import ActivityLog


@login_required
@require_capability('logs.read')
def activity_logs(request):
    logs = ActivityLog.objects.select_related('user').order_by('-created_at')[:50]

    data = [
        {
            'user': log.user.username,
            'action': log.action,
            'created_at': log.created_at.isoformat(),
        }
        for log in logs
    ]

    return JsonResponse(data, safe=False)
