from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.agendamentos.models import Appointment
from apps.usuarios.models import User

from .models import Service


class ServiceManagementTests(TestCase):
    def setUp(self):
        self.barber = User.objects.create_user("gestor@example.com", "SenhaForte#123", role=User.Role.BARBER)
        self.client.force_login(self.barber)

    def test_barber_can_create_service(self):
        response = self.client.post(reverse("service_manage"), {
            "name": "Corte", "price": "50.00", "duration_minutes": 40,
            "description": "Corte completo", "active": "on",
        })
        self.assertRedirects(response, reverse("service_manage"))
        self.assertTrue(Service.objects.filter(name="Corte", active=True).exists())

    def test_unused_service_is_deleted(self):
        service = Service.objects.create(name="Sobrancelha", price="20.00", duration_minutes=15)
        response = self.client.post(reverse("service_delete", args=[service.pk]))
        self.assertRedirects(response, reverse("service_manage"))
        self.assertFalse(Service.objects.filter(pk=service.pk).exists())

    def test_service_with_history_is_archived_and_hidden(self):
        customer = User.objects.create_user("cliente@example.com", "SenhaForte#123", role=User.Role.CLIENT)
        service = Service.objects.create(name="Corte histórico", price="50.00", duration_minutes=40)
        Appointment.objects.create(
            client=customer,
            barber=self.barber,
            service=service,
            date=timezone.localdate(),
            start_time="10:00",
            total_price=service.price,
            status=Appointment.Status.COMPLETED,
        )
        self.client.post(reverse("service_delete", args=[service.pk]))
        service.refresh_from_db()
        self.assertFalse(service.active)
        response = self.client.get(reverse("service_manage"))
        self.assertNotContains(response, "Corte histórico")
