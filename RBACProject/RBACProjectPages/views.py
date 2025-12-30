from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from accounts.utils.permissions import user_has_capability

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

@login_required
def about(request):
    return render(request, 'pages/about.html')

def dashboard(request):
    if not user_has_capability(request.user, "view_dashboard"):
        return HttpResponseForbidden("你沒有權限存取此頁面")
    
    return render(request, 'pages/dashboard.html')
