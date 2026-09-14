from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Agendado"
        COMPLETED = "completed", "Concluído"
        CANCELLED = "cancelled", "Cancelado"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="client_appointments")
    barber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="barber_appointments")
    service = models.ForeignKey("servicos.Service", on_delete=models.PROTECT, related_name="appointments")
    date = models.DateField("data")
    start_time = models.TimeField("horário")
    status = models.CharField("status", max_length=12, choices=Status.choices, default=Status.SCHEDULED)
    total_price = models.DecimalField("valor", max_digits=8, decimal_places=2)
    notes = models.TextField("observações", blank=True)
    rating = models.PositiveSmallIntegerField("avaliação", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["barber", "date", "start_time"],
                condition=models.Q(status="scheduled"),
                name="unique_active_barber_start",
            )
        ]

    @property
    def starts_at(self):
        return timezone.make_aware(datetime.combine(self.date, self.start_time))

    @property
    def ends_at(self):
        return self.starts_at + timedelta(minutes=self.service.duration_minutes)

    def clean(self):
        if self.client_id and self.client.role != "client":
            raise ValidationError({"client": "O usuário selecionado não é cliente."})
        if self.barber_id and self.barber.role != "barber":
            raise ValidationError({"barber": "O profissional selecionado não é barbeiro."})
        if self.rating is not None and not 1 <= self.rating <= 5:
            raise ValidationError({"rating": "A avaliação deve estar entre 1 e 5."})

    def save(self, *args, **kwargs):
        if self.service_id and not self.total_price:
            self.total_price = self.service.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} · {self.date:%d/%m/%Y} {self.start_time:%H:%M}"
