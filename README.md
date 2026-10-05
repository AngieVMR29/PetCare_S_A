# PetCare

Plataforma web para la gestión de servicios para mascotas (MVP). Conecta a propietarios de mascotas con proveedores de veterinaria, peluquería, paseo y cuidado temporal.

Proyecto integrador de Análisis y diseño de sistemas, Ingeniería de Software, Corporación Universitaria Iberoamericana.

**Equipo:** Sergio David Cifuentes Ramos · Angie Vanessa Mendieta Reyes

## Tecnologías

- Python 3 y Django 6.1 (backend y plantillas)
- HTML y CSS sencillo, adaptable a celular
- SQLite (base de datos del MVP)

## Estructura

| Carpeta | Contenido |
|---|---|
| `accounts/` | Usuarios con rol (propietario, proveedor, administrador), registro e inicio de sesión |
| `catalog/` | Perfil del proveedor, servicios, búsqueda con filtros y perfil detallado |
| `bookings/` | Solicitudes de reserva, estados, historial y notificaciones |
| `config/` | Configuración del proyecto y rutas |
| `templates/`, `static/` | Pantallas y estilos |
| `docs/` | Material del documento (prototipo de pantallas) |

## Cómo ejecutarlo en local

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Luego abrir http://127.0.0.1:8000. El panel de administración está en `/admin/`.

Pruebas automáticas (recorren el flujo completo del MVP):

```
python manage.py test
```

## Datos de prueba (pruebas de usuario)

Para cargar usuarios, servicios y una reserva de ejemplo (se puede repetir sin duplicar datos):

```
python manage.py seed_demo
```

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin_demo` | `Prueba123*` |
| Propietario | `propietario_demo` | `Prueba123*` |
| Proveedor | `proveedor_demo` | `Prueba123*` |

Incluye el negocio "Patitas Felices" (Chapinero) con 4 servicios (veterinaria, peluquería, paseo y cuidado temporal) y una solicitud de reserva pendiente del propietario para su perro Max.

Solo para entornos de prueba: no ejecutar en un sitio de producción.

## Estado del MVP

| Historia | Descripción | Estado |
|---|---|---|
| HU-01 | Registro con rol | Hecha |
| HU-02 | Inicio y cierre de sesión | Hecha |
| HU-03 | Perfil del proveedor y publicación de servicios | Hecha |
| HU-04 | Búsqueda por tipo | Hecha |
| HU-05 | Filtros por zona y precio | Hecha |
| HU-06 | Perfil detallado del proveedor | Hecha |
| HU-07 | Solicitud de reserva | Hecha |
| HU-08 | Aceptar o rechazar solicitudes | Hecha |
| HU-09 | Estado, historial y cancelación | Hecha |
| HU-10 | Notificaciones (en plataforma y por correo) | Hecha |
| HU-11 | Calificación y reseña | Pendiente (Sprint 4) |

Otros requisitos pendientes: recuperar contraseña (RF-03), registro de mascotas (RF-14) y moderación desde una vista propia (RF-16, hoy se hace desde `/admin/`).

## Pendiente para publicar (PythonAnywhere)

- Leer `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` desde variables de entorno.
- Definir `STATIC_ROOT` y ejecutar `collectstatic`.
- Configurar un servicio real de correo (hoy los correos salen por consola).
- Ejecutar `migrate` en el servidor, que crea una base de datos nueva y vacía.

## Notas

- Los correos de notificación se imprimen en la consola durante el desarrollo.
- `db.sqlite3` y `.venv/` no se suben al repositorio.
