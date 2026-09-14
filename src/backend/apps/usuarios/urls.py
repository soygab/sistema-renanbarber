from django.urls import path

from . import views

urlpatterns = [
    path("", views.entrypoint, name="entrypoint"),
    path("entrar/", views.login_view, name="login"),
    path("cadastro/", views.register_view, name="register"),
    path("sair/", views.logout_view, name="logout"),
]
