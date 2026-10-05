import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from bookings.models import BookingRequest
from catalog.models import ProviderProfile, Service

User = get_user_model()

PASSWORD = 'Prueba123*'

SERVICES = [
    ('vet', 'Consulta veterinaria general', 'Revisión completa y vacunación básica.', 60000),
    ('grooming', 'Baño y peluquería', 'Baño, corte de pelo y limpieza de oídos.', 45000),
    ('walk', 'Paseo de 1 hora', 'Paseo en parque cercano con recogida a domicilio.', 20000),
    ('sitting', 'Cuidado temporal por día', 'Cuidado en casa del proveedor, incluye alimentación.', 55000),
]


class Command(BaseCommand):
    help = 'Carga datos de prueba (usuarios, proveedor, servicios y una reserva). Es idempotente.'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username='admin_demo',
            defaults={'email': 'admin@petcare.test', 'is_staff': True, 'is_superuser': True},
        )
        owner, _ = User.objects.get_or_create(
            username='propietario_demo',
            defaults={'email': 'propietario@petcare.test', 'first_name': 'Laura', 'last_name': 'Gómez',
                      'role': User.Role.OWNER},
        )
        provider_user, _ = User.objects.get_or_create(
            username='proveedor_demo',
            defaults={'email': 'proveedor@petcare.test', 'first_name': 'Carlos', 'last_name': 'Ruiz',
                      'role': User.Role.PROVIDER},
        )
        for user in (admin, owner, provider_user):
            user.set_password(PASSWORD)
            user.save()

        profile, _ = ProviderProfile.objects.get_or_create(
            user=provider_user,
            defaults={'business_name': 'Patitas Felices', 'zone': 'Chapinero',
                      'description': 'Centro de servicios para mascotas.',
                      'schedule': 'Lun a Sáb, 8:00 a 18:00', 'phone': '3001234567'},
        )

        services = []
        for service_type, title, description, price in SERVICES:
            service, _ = Service.objects.get_or_create(
                provider=profile, title=title,
                defaults={'service_type': service_type, 'description': description, 'reference_price': price},
            )
            services.append(service)

        BookingRequest.objects.get_or_create(
            owner=owner, service=services[1], pet_name='Max',
            defaults={'pet_species': 'Perro - Golden Retriever',
                      'date': datetime.date.today() + datetime.timedelta(days=3),
                      'time': datetime.time(10, 0), 'notes': 'Es muy juguetón, pelo largo.'},
        )

        self.stdout.write(self.style.SUCCESS(f'Datos de prueba listos. Contraseña de todos: {PASSWORD}'))
        self.stdout.write('  admin_demo / propietario_demo / proveedor_demo')
