from django.http import HttpResponse
from accounts.decorators import require_capability

@require_capability('user.profile')
def profile(request):
    return HttpResponse('User Profile')
