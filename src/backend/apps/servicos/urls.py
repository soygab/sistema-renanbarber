from django.urls import path

from . import views

urlpatterns = [
    path("cliente/servicos/", views.service_list, name="service_list"),
    path("painel/servicos/", views.service_manage, name="service_manage"),
    path("painel/servicos/<int:pk>/editar/", views.service_manage, name="service_edit"),
    path("painel/servicos/<int:pk>/remover/", views.service_delete, name="service_delete"),
]
