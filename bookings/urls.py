from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('reservar/<int:service_id>/', views.create_booking, name='create'),
    path('mis-reservas/', views.my_bookings, name='my_bookings'),
    path('mis-reservas/<int:pk>/cancelar/', views.cancel_booking, name='cancel'),
    path('solicitudes/', views.received_requests, name='received'),
    path('solicitudes/<int:pk>/aceptar/', views.accept_booking, name='accept'),
    path('solicitudes/<int:pk>/rechazar/', views.reject_booking, name='reject'),
    path('notificaciones/', views.notifications, name='notifications'),
]
