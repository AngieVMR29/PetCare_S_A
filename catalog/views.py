from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from bookings.models import BookingRequest

from .forms import ProviderProfileForm, SearchForm, ServiceForm
from .models import ProviderProfile, Service


def home(request):
    return render(request, 'home.html', {'types': Service.Type.choices})


def search(request):
    """HU-04 / HU-05: búsqueda por tipo con filtros de zona y precio."""
    form = SearchForm(request.GET or None)
    services = Service.objects.filter(is_active=True).select_related('provider')
    if form.is_valid():
        data = form.cleaned_data
        if data['service_type']:
            services = services.filter(service_type=data['service_type'])
        if data['zone']:
            services = services.filter(provider__zone__icontains=data['zone'])
        if data['min_price'] is not None:
            services = services.filter(reference_price__gte=data['min_price'])
        if data['max_price'] is not None:
            services = services.filter(reference_price__lte=data['max_price'])
    return render(request, 'catalog/search.html', {'form': form, 'services': services})


def provider_detail(request, pk):
    """HU-06: perfil detallado del proveedor."""
    provider = get_object_or_404(ProviderProfile, pk=pk)
    services = provider.services.filter(is_active=True)
    return render(request, 'catalog/provider_detail.html', {'provider': provider, 'services': services})


# ---- Panel del proveedor -------------------------------------------------

@role_required(User.Role.PROVIDER)
def provider_dashboard(request):
    profile = getattr(request.user, 'provider_profile', None)
    if profile is None:
        messages.info(request, 'Completa tu perfil para poder publicar servicios.')
        return redirect('catalog:profile_edit')
    pending = BookingRequest.objects.filter(service__provider=profile, status=BookingRequest.Status.PENDING).count()
    return render(request, 'catalog/dashboard.html', {
        'profile': profile,
        'services': profile.services.all(),
        'pending': pending,
    })


@role_required(User.Role.PROVIDER)
def profile_edit(request):
    profile = getattr(request.user, 'provider_profile', None)
    form = ProviderProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Perfil guardado.')
        return redirect('catalog:dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Perfil del proveedor'})


@role_required(User.Role.PROVIDER)
def service_form(request, pk=None):
    profile = getattr(request.user, 'provider_profile', None)
    if profile is None:
        return redirect('catalog:profile_edit')
    service = get_object_or_404(Service, pk=pk, provider=profile) if pk else None
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.provider = profile
        obj.save()
        messages.success(request, 'Servicio guardado.')
        return redirect('catalog:dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Editar servicio' if pk else 'Nuevo servicio'})


@role_required(User.Role.PROVIDER)
def service_toggle(request, pk):
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=pk, provider__user=request.user)
        service.is_active = not service.is_active
        service.save(update_fields=['is_active'])
    return redirect('catalog:dashboard')
