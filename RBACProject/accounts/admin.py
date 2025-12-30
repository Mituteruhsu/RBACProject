from django.contrib import admin
from .models import User, Role, Permission, Capability
from import_export.admin import ImportExportMixin

@admin.register(User)
class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('username', 'email', 'display_roles', 'display_permissions', 'display_capabilities', 'is_active', 'is_staff', 'full_name')

    def save_model(self, request, obj, form, change):
        """
        如果密碼是明文，必須加密後再存
        """
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"
    
    def display_roles(self, obj):
        # 把多個角色名稱用逗號串起來
        return ", ".join([role.name for role in obj.roles.all()])
    
    display_roles.short_description = '角色'

    def display_permissions(self, obj):
        # 先取得該使用者所有角色，再取出角色的所有權限
        permissions = set()
        for role in obj.roles.all():
            for perm in role.permissions.all():
                permissions.add(perm.name)
        return ", ".join(permissions)
    display_permissions.short_description = "權限"

    def display_capabilities(self, obj):
        # 先取得所有權限，再取出 capabilities
        capabilities = set()
        for role in obj.roles.all():
            for perm in role.permissions.all():
                for cap in perm.capabilities.all():
                    capabilities.add(cap.name)
        return ", ".join(capabilities)
    display_capabilities.short_description = "功能"

@admin.register(Role)
class RoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'display_permissions')

    def display_permissions(self, obj):
        return ", ".join([p.name for p in obj.permissions.all()])
    display_permissions.short_description = "Permissions"

@admin.register(Permission)
class PermissionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'display_capabilities')

    def display_capabilities(self, obj):
        return ", ".join([c.name for c in obj.capabilities.all()])
    display_capabilities.short_description = "Capabilities"

@admin.register(Capability)
class CapabilityAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name','description')
