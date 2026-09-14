from django.db import models


class Service(models.Model):
    name = models.CharField("nome", max_length=100)
    description = models.TextField("descrição", blank=True)
    price = models.DecimalField("preço", max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveIntegerField("duração em minutos", default=30)
    active = models.BooleanField("ativo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "serviço"
        verbose_name_plural = "serviços"

    def __str__(self):
        return self.name
