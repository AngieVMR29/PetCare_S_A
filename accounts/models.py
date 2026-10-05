from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Propietario'
        PROVIDER = 'provider', 'Proveedor'
        ADMIN = 'admin', 'Administrador'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.OWNER)

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_provider(self):
        return self.role == self.Role.PROVIDER

    @property
    def is_platform_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def save(self, *args, **kwargs):
        # Los superusuarios creados por consola quedan como administradores.
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)
