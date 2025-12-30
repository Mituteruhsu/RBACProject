from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from accounts.services import user_has_capability

def require_capability(code: str):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not user_has_capability(request.user, code):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
