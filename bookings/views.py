from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import User
from catalog.models import Service

from .forms import BookingForm, RejectForm
from .models import BookingRequest, Notification
from .notifications import notify

Status = BookingRequest.Status


@role_required(User.Role.OWNER)
def create_booking(request, service_id):
    """HU-07: el propietario envía una solicitud de reserva."""
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.owner = request.user
        booking.service = service
        booking.save()
        notify(service.provider.user, f'Nueva solicitud de {request.user.first_name} para «{service.title}» el {booking.date}.')
        messages.success(request, 'Solicitud enviada. Quedó en estado Pendiente.')
        return redirect('bookings:my_bookings')
    return render(request, 'bookings/booking_form.html', {'form': form, 'service': service})


@role_required(User.Role.OWNER)
def my_bookings(request):
    """HU-09: estado e historial de solicitudes del propietario."""
    bookings = request.user.bookings.select_related('service__provider')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@role_required(User.Role.OWNER)
def cancel_booking(request, pk):
    booking = get_object_or_404(BookingRequest, pk=pk, owner=request.user)
    if request.method == 'POST' and booking.status in (Status.PENDING, Status.CONFIRMED) and booking.date >= timezone.localdate():
        booking.status = Status.CANCELLED
        booking.save(update_fields=['status'])
        notify(booking.service.provider.user, f'{request.user.first_name} canceló su solicitud de «{booking.service.title}» del {booking.date}.')
        messages.success(request, 'Solicitud cancelada.')
    return redirect('bookings:my_bookings')


@role_required(User.Role.PROVIDER)
def received_requests(request):
    """HU-08: solicitudes recibidas por el proveedor."""
    bookings = BookingRequest.objects.filter(service__provider__user=request.user).select_related('service', 'owner')
    return render(request, 'bookings/received.html', {'bookings': bookings, 'reject_form': RejectForm()})


def _respond(request, pk, new_status):
    booking = get_object_or_404(BookingRequest, pk=pk, service__provider__user=request.user)
    if request.method != 'POST' or booking.status != Status.PENDING:
        return redirect('bookings:received')
    booking.status = new_status
    msg = f'Tu solicitud de «{booking.service.title}» para el {booking.date} fue {booking.get_status_display().lower()}.'
    if new_status == Status.REJECTED:
        form = RejectForm(request.POST)
        booking.rejection_reason = form.cleaned_data['reason'] if form.is_valid() else ''
        if booking.rejection_reason:
            msg += f' Motivo: {booking.rejection_reason}'
    booking.save()
    notify(booking.owner, msg)
    messages.success(request, f'Solicitud {booking.get_status_display().lower()}.')
    return redirect('bookings:received')


@role_required(User.Role.PROVIDER)
def accept_booking(request, pk):
    return _respond(request, pk, Status.CONFIRMED)


@role_required(User.Role.PROVIDER)
def reject_booking(request, pk):
    return _respond(request, pk, Status.REJECTED)


@login_required
def notifications(request):
    items = list(request.user.notifications.all()[:50])
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'bookings/notifications.html', {'items': items})
