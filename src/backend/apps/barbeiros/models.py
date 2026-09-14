from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class BarberAvailability(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Segunda-feira"
        TUESDAY = 1, "Terça-feira"
        WEDNESDAY = 2, "Quarta-feira"
        THURSDAY = 3, "Quinta-feira"
        FRIDAY = 4, "Sexta-feira"
        SATURDAY = 5, "Sábado"
        SUNDAY = 6, "Domingo"

    barber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="availabilities")
    weekday = models.PositiveSmallIntegerField("dia", choices=Weekday.choices)
    start_time = models.TimeField("início")
    end_time = models.TimeField("fim")
    active = models.BooleanField("ativo", default=True)

    class Meta:
        ordering = ["weekday", "start_time"]
        constraints = [
            models.UniqueConstraint(fields=["barber", "weekday"], name="unique_barber_weekday")
        ]

    def clean(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("O horário final deve ser posterior ao inicial.")

    def __str__(self):
        return f"{self.barber} · {self.get_weekday_display()}"


class TimeBlock(models.Model):
    barber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="time_blocks")
    start = models.DateTimeField("início")
    end = models.DateTimeField("fim")
    reason = models.CharField("motivo", max_length=140, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start"]

    def clean(self):
        if self.start and self.end and self.end <= self.start:
            raise ValidationError("O fim do bloqueio deve ser posterior ao início.")

    def __str__(self):
        return f"{self.barber} · {self.start:%d/%m/%Y %H:%M}"
