from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "E-mail ou senha inválidos.",
        "inactive": "Este acesso está desativado.",
    }
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"placeholder": "contato@suabarbearia.com", "autocomplete": "email"}))
    password = forms.CharField(label="Senha", strip=False, widget=forms.PasswordInput(attrs={"placeholder": "••••••••", "autocomplete": "current-password"}))


class ClientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")
        labels = {"email": "E-mail", "phone": "Telefone"}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user


class BarberCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "commission_rate")
        labels = {"email": "E-mail", "phone": "Telefone", "commission_rate": "Comissão (%)"}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.BARBER
        if commit:
            user.save()
        return user
