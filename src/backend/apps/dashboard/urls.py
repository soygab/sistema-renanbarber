from django.urls import path

from . import views

urlpatterns = [
    path("cliente/", views.client_home, name="client_home"),
    path("painel/", views.barber_home, name="barber_home"),
]
