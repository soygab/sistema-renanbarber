from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.barbeiros.models import BarberAvailability, TimeBlock
from apps.servicos.models import Service
from apps.usuarios.models import User
from utils.permissions import barber_required, client_required

from .forms import AppointmentForm
from .models import Appointment


@client_required
def client_appointments(request):
    today = timezone.localdate()
    records = Appointment.objects.filter(client=request.user).select_related("service", "barber")
    upcoming = records.filter(status=Appointment.Status.SCHEDULED, date__gte=today)
    history = records.exclude(pk__in=upcoming.values("pk")).order_by("-date", "-start_time")
    return render(request, "meus-agendamentos.html", {"upcoming": upcoming, "history": history})


@client_required
def appointment_create(request):
    initial = {"service": request.GET.get("servico"), "barber": request.GET.get("barbeiro")}
    form = AppointmentForm(request.POST or None, client=request.user, initial=initial)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Agendamento confirmado com sucesso.")
        return redirect("client_appointments")
    return render(request, "agendar.html", {"form": form, "editing": False})


@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, status=Appointment.Status.SCHEDULED)
    is_owner = request.user.role == User.Role.CLIENT and appointment.client_id == request.user.id
    if not (is_owner or request.user.role == User.Role.BARBER or request.user.is_superuser):
        return redirect("entrypoint")
    form = AppointmentForm(request.POST or None, instance=appointment, client=appointment.client)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Agendamento remarcado com sucesso.")
        return redirect("barber_appointments" if request.user.role == User.Role.BARBER else "client_appointments")
    return render(request, "agendar.html", {"form": form, "editing": True, "appointment": appointment})


@require_POST
@login_required
def appointment_action(request, pk, action):
    appointment = get_object_or_404(Appointment, pk=pk)
    is_owner = request.user.role == User.Role.CLIENT and appointment.client_id == request.user.id
    is_barber = request.user.role == User.Role.BARBER or request.user.is_superuser
    if not (is_owner or is_barber):
        return redirect("entrypoint")
    if action == "cancel" and appointment.status == Appointment.Status.SCHEDULED:
        appointment.status = Appointment.Status.CANCELLED
        messages.success(request, "Agendamento cancelado.")
    elif action == "complete" and is_barber and appointment.status == Appointment.Status.SCHEDULED:
        appointment.status = Appointment.Status.COMPLETED
        messages.success(request, "Atendimento marcado como concluído.")
    else:
        messages.error(request, "Essa alteração não está disponível.")
        return redirect("barber_appointments" if is_barber else "client_appointments")
    appointment.save(update_fields=["status", "updated_at"])
    return redirect("barber_appointments" if is_barber else "client_appointments")


@require_POST
@client_required
def appointment_rate(request, pk):
    appointment = get_object_or_404(
        Appointment, pk=pk, client=request.user, status=Appointment.Status.COMPLETED
    )
    try:
        rating = int(request.POST.get("rating", ""))
    except ValueError:
        rating = 0
    if rating not in range(1, 6):
        messages.error(request, "Escolha uma nota entre 1 e 5.")
    else:
        appointment.rating = rating
        appointment.save(update_fields=["rating", "updated_at"])
        messages.success(request, "Obrigado pela avaliação!")
    return redirect("client_appointments")


@barber_required
def barber_appointments(request):
    try:
        selected_date = datetime.strptime(request.GET.get("data", ""), "%Y-%m-%d").date()
    except ValueError:
        selected_date = timezone.localdate()
    barber_id = request.GET.get("barbeiro")
    records = Appointment.objects.filter(date=selected_date).select_related("client", "barber", "service")
    if barber_id:
        records = records.filter(barber_id=barber_id)
    return render(request, "barbeiro-agendamentos.html", {
        "appointments": records,
        "selected_date": selected_date,
        "barbers": User.objects.filter(role=User.Role.BARBER, is_active=True),
        "selected_barber": barber_id or "",
    })


@client_required
def available_slots(request):
    try:
        barber = User.objects.get(pk=request.GET["barber"], role=User.Role.BARBER, is_active=True)
        service = Service.objects.get(pk=request.GET["service"], active=True)
        date = datetime.strptime(request.GET["date"], "%Y-%m-%d").date()
    except (KeyError, ValueError, User.DoesNotExist, Service.DoesNotExist):
        return JsonResponse({"slots": []})
    availability = BarberAvailability.objects.filter(barber=barber, weekday=date.weekday(), active=True).first()
    if not availability:
        return JsonResponse({"slots": []})

    cursor = timezone.make_aware(datetime.combine(date, availability.start_time))
    closing = timezone.make_aware(datetime.combine(date, availability.end_time))
    duration = timedelta(minutes=service.duration_minutes)
    existing_query = Appointment.objects.filter(barber=barber, date=date, status=Appointment.Status.SCHEDULED).select_related("service")
    if request.GET.get("appointment", "").isdigit():
        existing_query = existing_query.exclude(pk=request.GET["appointment"])
    existing = list(existing_query)
    blocks = list(TimeBlock.objects.filter(barber=barber, start__lt=closing, end__gt=cursor))
    slots = []
    while cursor + duration <= closing:
        slot_end = cursor + duration
        occupied = any(cursor < item.ends_at and slot_end > item.starts_at for item in existing)
        blocked = any(cursor < block.end and slot_end > block.start for block in blocks)
        if cursor > timezone.now() and not occupied and not blocked:
            slots.append(cursor.strftime("%H:%M"))
        cursor += timedelta(minutes=30)
    return JsonResponse({"slots": slots})
