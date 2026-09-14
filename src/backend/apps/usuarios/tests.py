from django.test import TestCase
from django.urls import reverse

from .models import User


class AuthenticationTests(TestCase):
    def test_login_checks_password_and_routes_client(self):
        User.objects.create_user("cliente@example.com", "SenhaForte#123", role=User.Role.CLIENT)
        invalid = self.client.post(reverse("login"), {"username": "cliente@example.com", "password": "incorreta"})
        self.assertEqual(invalid.status_code, 200)
        self.assertContains(invalid, "E-mail ou senha inválidos")
        valid = self.client.post(reverse("login"), {"username": "cliente@example.com", "password": "SenhaForte#123"}, follow=True)
        self.assertEqual(valid.resolver_match.url_name, "client_home")

    def test_registration_creates_authenticated_client(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Ana", "last_name": "Silva", "email": "ana@example.com",
            "phone": "11999999999", "password1": "SenhaForte#123", "password2": "SenhaForte#123",
        })
        self.assertRedirects(response, reverse("client_home"))
        self.assertEqual(User.objects.get(email="ana@example.com").role, User.Role.CLIENT)

    def test_entrypoint_routes_each_role(self):
        client = User.objects.create_user("cliente@example.com", "SenhaForte#123", role=User.Role.CLIENT)
        self.client.force_login(client)
        self.assertRedirects(self.client.get(reverse("entrypoint")), reverse("client_home"))
        self.client.logout()
        barber = User.objects.create_user("barbeiro@example.com", "SenhaForte#123", role=User.Role.BARBER)
        self.client.force_login(barber)
        self.assertRedirects(self.client.get(reverse("entrypoint")), reverse("barber_home"))

    def test_client_cannot_open_barber_area(self):
        client = User.objects.create_user("cliente@example.com", "SenhaForte#123", role=User.Role.CLIENT)
        self.client.force_login(client)
        self.assertEqual(self.client.get(reverse("barber_home")).status_code, 403)
