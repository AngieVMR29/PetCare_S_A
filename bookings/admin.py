from django.contrib import admin

from .models import BookingRequest, Notification


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('pet_name', 'service', 'owner', 'date', 'status')
    list_filter = ('status',)


admin.site.register(Notification)
