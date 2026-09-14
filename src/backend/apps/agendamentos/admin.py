from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("date", "start_time", "client", "barber", "service", "status", "total_price")
    list_filter = ("status", "date", "barber")
    search_fields = ("client__email", "barber__email", "service__name")
