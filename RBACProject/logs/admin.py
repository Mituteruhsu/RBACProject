from django.contrib import admin
from .models import ActivityLog
from .utils import parse_browser, get_status_code
from import_export.admin import ImportExportMixin
from import_export.formats.base_formats import CSV

@admin.register(ActivityLog)
class ActivityLogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'is_anonymous', 'browser', 'ip_address', 'method', 'action', 'path', 'created_at',)
    list_select_related = ('user',)
    ordering = ('-created_at',)
    readonly_fields = [f.name for f in ActivityLog._meta.fields]
    
    # 決定「是否顯示在 Admin 首頁」
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.has_capability('logs.read')

    # 決定「是否能進入列表 / 查看」
    def has_view_permission(self, request, obj=None):
        """
        只有具備 logs.read capability 的使用者可以看
        """
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.has_capability('logs.read')
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def is_anonymous(self, obj):
            return obj.user is None
    is_anonymous.boolean = True
    is_anonymous.short_description = "Anonymous"

    def browser(self, obj):
        return parse_browser(obj.user_agent)
    
    def short_path(self, obj):
        return obj.path[:40] + '...' if len(obj.path) > 40 else obj.path
    
    def status_code(self, obj):
        return get_status_code(obj.extra)
    
    # 匯出設定，如果不設定會顯示選單
    # formats = [CSV]