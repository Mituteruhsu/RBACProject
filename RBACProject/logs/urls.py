from django.urls import path
from .views import activity_logs

urlpatterns = [
    path('activity/', activity_logs),
]
