from django.core.mail import send_mail

from .models import Notification


def notify(user, message):
    """Crea un aviso en la plataforma y envía un correo (consola en desarrollo)."""
    Notification.objects.create(user=user, message=message)
    if user.email:
        send_mail('PetCare: actualización de tu solicitud', message, None, [user.email], fail_silently=True)
