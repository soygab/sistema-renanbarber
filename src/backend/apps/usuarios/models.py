from decimal import Decimal

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Role.BARBER)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Cliente"
        BARBER = "barber", "Barbeiro"

    username = None
    email = models.EmailField("e-mail", unique=True)
    role = models.CharField("perfil", max_length=10, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField("telefone", max_length=20, blank=True)
    commission_rate = models.DecimalField(
        "comissão (%)", max_digits=5, decimal_places=2, default=Decimal("40.00")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def display_name(self):
        return self.get_full_name() or self.email.split("@")[0]

    @property
    def initials(self):
        names = self.display_name.split()
        return "".join(name[0] for name in names[:2]).upper()

    def __str__(self):
        return self.display_name
