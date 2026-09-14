from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from apps.barbeiros.models import BarberAvailability, TimeBlock
from apps.servicos.models import Service
from apps.usuarios.models import User

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("service", "barber", "date", "start_time", "notes")
        labels = {"service": "Serviço", "barber": "Barbeiro", "date": "Data", "start_time": "Horário", "notes": "Observações"}
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "step": 1800}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Alguma preferência?"}),
        }

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop("client", None)
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(active=True)
        self.fields["barber"].queryset = User.objects.filter(role=User.Role.BARBER, is_active=True).order_by("first_name")
        self.fields["date"].widget.attrs["min"] = timezone.localdate().isoformat()

    def clean(self):
        cleaned = super().clean()
        service, barber = cleaned.get("service"), cleaned.get("barber")
        date, start_time = cleaned.get("date"), cleaned.get("start_time")
        if not all((service, barber, date, start_time)):
            return cleaned

        start = timezone.make_aware(datetime.combine(date, start_time))
        end = start + timedelta(minutes=service.duration_minutes)
        if start <= timezone.now():
            raise forms.ValidationError("Escolha um horário futuro.")

        availability = BarberAvailability.objects.filter(barber=barber, weekday=date.weekday(), active=True).first()
        if not availability:
            raise forms.ValidationError("O barbeiro não atende nesse dia.")
        available_start = timezone.make_aware(datetime.combine(date, availability.start_time))
        available_end = timezone.make_aware(datetime.combine(date, availability.end_time))
        if start < available_start or end > available_end:
            raise forms.ValidationError("O horário está fora da disponibilidade do barbeiro.")
        if TimeBlock.objects.filter(barber=barber, start__lt=end, end__gt=start).exists():
            raise forms.ValidationError("Esse período foi bloqueado pelo barbeiro.")

        existing = Appointment.objects.filter(barber=barber, date=date, status=Appointment.Status.SCHEDULED).select_related("service")
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        for appointment in existing:
            if start < appointment.ends_at and end > appointment.starts_at:
                raise forms.ValidationError("Esse horário acabou de ser ocupado. Escolha outro.")
        return cleaned

    def save(self, commit=True):
        appointment = super().save(commit=False)
        if self.client:
            appointment.client = self.client
        appointment.total_price = appointment.service.price
        if commit:
            appointment.save()
        return appointment
