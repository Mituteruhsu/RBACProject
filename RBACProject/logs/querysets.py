from django.db import models

class ActivityLogQuerySet(models.QuerySet):
    def readable(self):
        # 這裡可以做 select_related 提升效能
        return self.select_related('user')
    def anonymous(self):
        return self.filter(user__isnull=True)

    def by_action(self, action: str):
        return self.filter(action=action)
