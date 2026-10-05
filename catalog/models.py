from django.conf import settings
from django.db import models


class ProviderProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provider_profile')
    business_name = models.CharField('Nombre del negocio', max_length=120)
    description = models.TextField('Descripción', blank=True)
    zone = models.CharField('Zona / barrio', max_length=100)
    schedule = models.CharField('Horario', max_length=120, blank=True, help_text='Ej: Lun a Sáb, 8:00 a 18:00')
    phone = models.CharField('Teléfono', max_length=30, blank=True)

    def __str__(self):
        return self.business_name


class Service(models.Model):
    class Type(models.TextChoices):
        VET = 'vet', 'Veterinaria'
        GROOMING = 'grooming', 'Peluquería'
        WALK = 'walk', 'Paseo'
        SITTING = 'sitting', 'Cuidado temporal'

    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField('Tipo de servicio', max_length=10, choices=Type.choices)
    title = models.CharField('Título', max_length=120)
    description = models.TextField('Descripción', blank=True)
    reference_price = models.DecimalField('Precio de referencia (COP)', max_digits=10, decimal_places=0)
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.provider})'
