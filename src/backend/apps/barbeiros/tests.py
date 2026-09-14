from django.test import TestCase
from django.urls import reverse

from apps.usuarios.models import User

from .models import BarberAvailability


class BarberManagementTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user("gestor@example.com", "SenhaForte#123", role=User.Role.BARBER)
        self.client.force_login(self.manager)

    def test_barber_can_add_professional_with_default_schedule(self):
        response = self.client.post(reverse("barber_team"), {
            "first_name": "Carlos", "last_name": "Souza", "email": "carlos@example.com",
            "phone": "11988887777", "commission_rate": "35.00",
            "password1": "SenhaForte#123", "password2": "SenhaForte#123",
        })
        self.assertRedirects(response, reverse("barber_team"))
        barber = User.objects.get(email="carlos@example.com")
        self.assertEqual(barber.role, User.Role.BARBER)
        self.assertEqual(BarberAvailability.objects.filter(barber=barber).count(), 7)

    def test_barber_pages_render(self):
        for name in ("barber_home", "barber_team", "barber_hours"):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)
