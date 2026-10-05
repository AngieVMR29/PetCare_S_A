from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class PetCareUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (('PetCare', {'fields': ('role',)}),)
