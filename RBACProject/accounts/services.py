from logs.models import ActivityLog
from logs.utils import get_client_ip

def user_has_capability(user, capability_code: str) -> bool:
    if not user.is_authenticated:
        return False

    return user.has_capability(capability_code)

def log_action(request, action, extra=None):
    ActivityLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        path=request.path,
        method=request.method,
        action=action,
        extra=extra or {}
    )