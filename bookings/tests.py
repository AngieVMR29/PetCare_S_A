import datetime

from django.test import Client, TestCase

from accounts.models import User
from bookings.models import BookingRequest, Notification
from catalog.models import Service

PWD = 'Clave12345x'


class MvpFlowTests(TestCase):
    """Flujo completo del MVP: registro, publicar, buscar, reservar, aceptar, cancelar."""

    def test_full_flow(self):
        prov, owner = Client(), Client()

        # HU-01 registro de ambos roles
        r = prov.post('/cuenta/registro/', {'first_name': 'Vet', 'email': 'p@x.co', 'role': 'provider', 'password1': PWD, 'password2': PWD})
        self.assertEqual(r.status_code, 302)
        r = owner.post('/cuenta/registro/', {'first_name': 'Ana', 'email': 'o@x.co', 'role': 'owner', 'password1': PWD, 'password2': PWD})
        self.assertEqual(r.status_code, 302)

        # HU-03 perfil y servicio
        self.assertEqual(prov.post('/panel/perfil/', {'business_name': 'Vet Feliz', 'zone': 'Chapinero'}).status_code, 302)
        self.assertEqual(prov.post('/panel/servicios/nuevo/', {'service_type': 'vet', 'title': 'Consulta', 'reference_price': '50000', 'is_active': 'on'}).status_code, 302)
        service = Service.objects.get()

        # HU-04/05/06 búsqueda, filtros y perfil
        self.assertContains(owner.get('/buscar/?service_type=vet&zone=chapi'), 'Consulta')
        self.assertNotContains(owner.get('/buscar/?service_type=walk'), 'Consulta')
        self.assertContains(owner.get(f'/proveedores/{service.provider.pk}/'), 'Solicitar servicio')

        # HU-07 solicitud (fecha pasada rechazada)
        past = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        owner.post(f'/reservar/{service.pk}/', {'pet_name': 'Rex', 'pet_species': 'Perro', 'date': past, 'time': '10:00'})
        self.assertEqual(BookingRequest.objects.count(), 0)
        future = (datetime.date.today() + datetime.timedelta(days=3)).isoformat()
        r = owner.post(f'/reservar/{service.pk}/', {'pet_name': 'Rex', 'pet_species': 'Perro', 'date': future, 'time': '10:00'})
        self.assertEqual(r.status_code, 302)
        booking = BookingRequest.objects.get()
        self.assertEqual(booking.status, 'pending')

        # HU-08 / HU-10 el proveedor acepta y el propietario recibe aviso
        self.assertEqual(prov.get('/panel/').status_code, 200)
        self.assertContains(prov.get('/solicitudes/'), 'Rex')
        prov.post(f'/solicitudes/{booking.pk}/aceptar/')
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'confirmed')
        self.assertTrue(Notification.objects.filter(user__email='o@x.co').exists())

        # HU-09 cancelar
        self.assertEqual(owner.get('/mis-reservas/').status_code, 200)
        owner.post(f'/mis-reservas/{booking.pk}/cancelar/')
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

        # RNF-06 control por rol
        self.assertEqual(owner.get('/solicitudes/').status_code, 403)
        self.assertTrue(User.objects.filter(email='p@x.co', role='provider').exists())
