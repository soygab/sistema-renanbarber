from datetime import time, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.barbeiros.models import BarberAvailability
from apps.servicos.models import Service
from apps.usuarios.models import User

from .models import Appointment


class AppointmentFlowTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user("cliente@example.com", "SenhaForte#123", role=User.Role.CLIENT)
        self.other_customer = User.objects.create_user("outro@example.com", "SenhaForte#123", role=User.Role.CLIENT)
        self.barber = User.objects.create_user("barbeiro@example.com", "SenhaForte#123", role=User.Role.BARBER)
        self.service = Service.objects.create(name="Corte", price="50.00", duration_minutes=40)
        self.date = timezone.localdate() + timedelta(days=7)
        BarberAvailability.objects.create(barber=self.barber, weekday=self.date.weekday(), start_time=time(9), end_time=time(18))

    def test_client_chooses_barber_and_creates_appointment(self):
        self.client.force_login(self.customer)
        response = self.client.post(reverse("appointment_create"), {
            "service": self.service.pk, "barber": self.barber.pk,
            "date": self.date.isoformat(), "start_time": "10:00", "notes": "",
        })
        self.assertRedirects(response, reverse("client_appointments"))
        item = Appointment.objects.get()
        self.assertEqual(item.barber, self.barber)
        self.assertEqual(item.client, self.customer)

    def test_conflicting_appointment_is_rejected(self):
        Appointment.objects.create(client=self.customer, barber=self.barber, service=self.service, date=self.date, start_time=time(10), total_price=self.service.price)
        self.client.force_login(self.other_customer)
        response = self.client.post(reverse("appointment_create"), {
            "service": self.service.pk, "barber": self.barber.pk,
            "date": self.date.isoformat(), "start_time": "10:30", "notes": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertContains(response, "horário acabou de ser ocupado")

    def test_available_slots_omit_booked_time(self):
        Appointment.objects.create(client=self.customer, barber=self.barber, service=self.service, date=self.date, start_time=time(10), total_price=self.service.price)
        self.client.force_login(self.other_customer)
        response = self.client.get(reverse("available_slots"), {"barber": self.barber.pk, "service": self.service.pk, "date": self.date.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("10:00", response.json()["slots"])
        self.assertNotIn("10:30", response.json()["slots"])

    def test_client_pages_render(self):
        self.client.force_login(self.customer)
        for name in ("client_home", "client_appointments", "service_list", "appointment_create"):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_barber_daily_agenda_renders(self):
        self.client.force_login(self.barber)
        self.assertEqual(self.client.get(reverse("barber_appointments")).status_code, 200)

    def test_client_can_rate_completed_appointment(self):
        appointment = Appointment.objects.create(
            client=self.customer, barber=self.barber, service=self.service,
            date=self.date, start_time=time(10), total_price=self.service.price,
            status=Appointment.Status.COMPLETED,
        )
        self.client.force_login(self.customer)
        response = self.client.post(reverse("appointment_rate", args=[appointment.pk]), {"rating": "5"})
        self.assertRedirects(response, reverse("client_appointments"))
        appointment.refresh_from_db()
        self.assertEqual(appointment.rating, 5)
