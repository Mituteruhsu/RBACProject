from django.urls import path
from accounts.views.user import profile

urlpatterns = [
    path('profile/', profile),
]
