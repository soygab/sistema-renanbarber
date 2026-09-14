from django.urls import path

from . import views

urlpatterns = [
    path("painel/equipe/", views.barber_team, name="barber_team"),
    path("painel/equipe/<int:pk>/alternar/", views.barber_toggle, name="barber_toggle"),
    path("painel/horarios/", views.barber_hours, name="barber_hours"),
    path("painel/bloqueios/<int:pk>/remover/", views.block_delete, name="block_delete"),
]
