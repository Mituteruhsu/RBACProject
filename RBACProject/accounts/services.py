from logs.models import ActivityLog

def user_has_capability(user, capability_code: str) -> bool:
    if not user.is_authenticated:
        return False

    return user.has_capability(capability_code)


def log_action(user, action: str):
    ActivityLog.objects.create(
        user=user,
        action=action
    )
