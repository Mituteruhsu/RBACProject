from django.contrib import admin
from .models import User, Role, Permission, Capability

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'full_name')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_permissions')

    def display_permissions(self, obj):
        return ", ".join([p.name for p in obj.permissions.all()])
    display_permissions.short_description = "Permissions"

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_capabilities')

    def display_capabilities(self, obj):
        return ", ".join([c.name for c in obj.capabilities.all()])
    display_capabilities.short_description = "Capabilities"

@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ('name','description')
