def user_has_capability(user, capability_name):
    if not user.is_authenticated:
        return False
    # 超級管理員直接放行
    if user.is_superuser:
        return True
        
    return user.roles.filter(
        permissions__capabilities__name=capability_name
    ).exists()
