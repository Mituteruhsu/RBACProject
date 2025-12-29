from django.http import HttpResponse
from accounts.decorators import require_capability
from accounts.services import log_action

@require_capability('user.profile')
def profile(request):
    # login success
    log_action(request, 'login_success')
    return HttpResponse('User Profile')
