from datetime import time

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.usuarios.forms import BarberCreationForm
from apps.usuarios.models import User
from utils.permissions import barber_required

from .forms import AvailabilityForm, TimeBlockForm
from .models import BarberAvailability, TimeBlock


@barber_required
def barber_team(request):
    form = BarberCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        barber = form.save()
        defaults = []
        for weekday in range(7):
            defaults.append(BarberAvailability(
                barber=barber,
                weekday=weekday,
                start_time=time(8 if weekday == 5 else 9),
                end_time=time(17 if weekday == 5 else 19),
                active=weekday < 6,
            ))
        BarberAvailability.objects.bulk_create(defaults)
        messages.success(request, "Barbeiro adicionado à equipe.")
        return redirect("barber_team")
    return render(request, "barbeiro-equipe.html", {
        "barbers": User.objects.filter(role=User.Role.BARBER).order_by("first_name"),
        "form": form,
    })


@require_POST
@barber_required
def barber_toggle(request, pk):
    barber = get_object_or_404(User, pk=pk, role=User.Role.BARBER)
    if barber == request.user:
        messages.error(request, "Você não pode desativar o próprio acesso.")
    else:
        barber.is_active = not barber.is_active
        barber.save(update_fields=["is_active"])
        messages.success(request, "Status do profissional atualizado.")
    return redirect("barber_team")


@barber_required
def barber_hours(request):
    barbers = User.objects.filter(role=User.Role.BARBER, is_active=True).order_by("first_name")
    selected = get_object_or_404(barbers, pk=request.GET.get("barbeiro", request.user.pk))
    availability = {item.weekday: item for item in BarberAvailability.objects.filter(barber=selected)}
    rows = []
    for weekday, label in BarberAvailability.Weekday.choices:
        rows.append({"weekday": weekday, "label": label, "value": availability.get(weekday)})

    availability_form = AvailabilityForm(request.POST or None) if request.POST.get("action") == "availability" else AvailabilityForm()
    block_form = TimeBlockForm(request.POST or None) if request.POST.get("action") == "block" else TimeBlockForm()
    if request.method == "POST" and request.POST.get("action") == "availability" and availability_form.is_valid():
        data = availability_form.cleaned_data
        item, _ = BarberAvailability.objects.update_or_create(
            barber=selected, weekday=data["weekday"],
            defaults={"start_time": data["start_time"], "end_time": data["end_time"], "active": data["active"]},
        )
        item.full_clean()
        messages.success(request, "Disponibilidade atualizada.")
        return redirect(f"/painel/horarios/?barbeiro={selected.pk}")
    if request.method == "POST" and request.POST.get("action") == "block" and block_form.is_valid():
        block = block_form.save(commit=False)
        block.barber = selected
        block.full_clean()
        block.save()
        messages.success(request, "Período bloqueado.")
        return redirect(f"/painel/horarios/?barbeiro={selected.pk}")

    return render(request, "barbeiro-horarios.html", {
        "barbers": barbers,
        "selected": selected,
        "rows": rows,
        "availability_form": availability_form,
        "block_form": block_form,
        "blocks": TimeBlock.objects.filter(barber=selected).order_by("start")[:20],
    })


@require_POST
@barber_required
def block_delete(request, pk):
    block = get_object_or_404(TimeBlock, pk=pk)
    barber_id = block.barber_id
    block.delete()
    messages.success(request, "Bloqueio removido.")
    return redirect(f"/painel/horarios/?barbeiro={barber_id}")
