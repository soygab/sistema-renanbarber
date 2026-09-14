from django.contrib import admin

from .models import BarberAvailability, TimeBlock


admin.site.register(BarberAvailability)
admin.site.register(TimeBlock)
