from django.urls import path

from . import views

urlpatterns = [
    path("cliente/agendamentos/", views.client_appointments, name="client_appointments"),
    path("cliente/agendar/", views.appointment_create, name="appointment_create"),
    path("agendamentos/<int:pk>/remarcar/", views.appointment_edit, name="appointment_edit"),
    path("agendamentos/<int:pk>/avaliar/", views.appointment_rate, name="appointment_rate"),
    path("agendamentos/<int:pk>/<str:action>/", views.appointment_action, name="appointment_action"),
    path("painel/agendamentos/", views.barber_appointments, name="barber_appointments"),
    path("api/horarios-disponiveis/", views.available_slots, name="available_slots"),
]
