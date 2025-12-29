import time
from django.conf import settings
from .models import ActivityLog
from .utils import get_client_ip, is_bot
from .constants import LogAction
from .services import log_activity

class ActivityLogMiddleware:
    """
    Session-based throttled activity logger
    """
    DEFAULT_COOLDOWN = 15  # 秒

    def __init__(self, get_response):
        self.get_response = get_response
        self.cooldown = getattr(
            settings,
            'ACTIVITY_LOG_COOLDOWN',
            self.DEFAULT_COOLDOWN
        )

    def __call__(self, request):
        response = self.get_response(request)

        # 1 排除不該記錄的路徑
        if self._should_ignore(request):
            return response
        
        # 2 Bot 直接略過
        if is_bot(request.META.get('HTTP_USER_AGENT', '')):
            return response

        # 3 節流判斷
        if not self._should_log(request, LogAction.PAGE_VIEW):
            return response

        data = {
                'user_id': request.user.id if request.user.is_authenticated else None,
                'ip_address': get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'path': request.path,
                'method': request.method,
                'action': LogAction.PAGE_VIEW,
                'extra': {'status_code': response.status_code},
            }

        log_activity(**data)

        return response

    # ======================
    # private methods
    # ======================

    def _should_ignore(self, request) -> bool:
        """
        排除 static / admin / health check
        """
        path = request.path
        return (
            path.startswith('/static/')
            or path.startswith('/admin/')
            or path.startswith('/django-admin/')
        )

    def _should_log(self, request, action: str) -> bool:
        """
        Session + path + action 節流
        """
        if not request.session.session_key:
            request.session.save()

        key = f'activity_log:{action}:{request.path}'
        now = int(time.time())

        last_time = request.session.get(key)
        if last_time and now - last_time < self.cooldown:
            return False

        request.session[key] = now
        return True
    