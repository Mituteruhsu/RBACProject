from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')
    list_select_related = ('user',)
    ordering = ('-created_at',)
    readonly_fields = ('user', 'action', 'created_at')

    def has_view_permission(self, request, obj=None):
        """
        只有具備 logs.read capability 的使用者可以看
        """
        if not request.user.is_authenticated:
            return False
        return request.user.has_capability('logs.read')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
