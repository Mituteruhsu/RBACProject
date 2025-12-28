from django.http import HttpResponse
from accounts.decorators import require_capability


@require_capability('admin.dashboard')
def dashboard(request):
    return HttpResponse('Admin Dashboard')
