from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.usuarios.urls")),
    path("", include("apps.dashboard.urls")),
    path("", include("apps.servicos.urls")),
    path("", include("apps.agendamentos.urls")),
    path("", include("apps.barbeiros.urls")),
]
