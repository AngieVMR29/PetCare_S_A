from django.conf import settings
from django.db import models

from catalog.models import Service


class BookingRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        CONFIRMED = 'confirmed', 'Confirmada'
        REJECTED = 'rejected', 'Rechazada'
        CANCELLED = 'cancelled', 'Cancelada'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    pet_name = models.CharField('Nombre de la mascota', max_length=80)
    pet_species = models.CharField('Especie / raza', max_length=80)
    date = models.DateField('Fecha')
    time = models.TimeField('Hora')
    notes = models.TextField('Notas', blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.CharField('Motivo del rechazo', max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.pet_name} – {self.service.title} ({self.get_status_display()})'


class Notification(models.Model):
    """HU-10: avisos dentro de la plataforma (además del correo)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
