from django.contrib import admin

from .models import ProviderProfile, Service


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'zone', 'user')
    search_fields = ('business_name', 'zone')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'provider', 'reference_price', 'is_active')
    list_filter = ('service_type', 'is_active')
