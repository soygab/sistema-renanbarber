from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ClientRegistrationForm, LoginForm


def entrypoint(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return redirect("barber_home" if request.user.role == "barber" or request.user.is_superuser else "client_home")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("entrypoint")
    form = LoginForm(request, data=request.POST or None)
    register_form = ClientRegistrationForm()
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        next_url = request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect("entrypoint")
    return render(request, "login.html", {"form": form, "register_form": register_form, "active_tab": "login"})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("entrypoint")
    register_form = ClientRegistrationForm(request.POST or None)
    form = LoginForm(request)
    if request.method == "POST" and register_form.is_valid():
        user = register_form.save()
        login(request, user)
        messages.success(request, "Sua conta foi criada com sucesso.")
        return redirect("client_home")
    return render(request, "login.html", {"form": form, "register_form": register_form, "active_tab": "register"})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")
