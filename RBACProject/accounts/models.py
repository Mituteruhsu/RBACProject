from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# Capability
# =========================
class Capability(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# =========================
# Permission
# =========================
class Permission(models.Model):
    name = models.CharField(max_length=50)
    capabilities = models.ManyToManyField(Capability)

    def __str__(self):
        return self.name


# =========================
# Role
# =========================
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name


# =========================
# User
# =========================
class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True)

    def has_capability(self, name: str) -> bool:
        if not self.is_authenticated:
            return False

        return Capability.objects.filter(
            permission__role__user=self,
            name=name
        ).exists()