from django.test import TestCase
from django.urls import reverse

from apps.usuarios.models import User

from .models import Service


class ServiceManagementTests(TestCase):
    def test_barber_can_create_service(self):
        barber = User.objects.create_user("gestor@example.com", "SenhaForte#123", role=User.Role.BARBER)
        self.client.force_login(barber)
        response = self.client.post(reverse("service_manage"), {
            "name": "Corte", "price": "50.00", "duration_minutes": 40,
            "description": "Corte completo", "active": "on",
        })
        self.assertRedirects(response, reverse("service_manage"))
        self.assertTrue(Service.objects.filter(name="Corte", active=True).exists())
