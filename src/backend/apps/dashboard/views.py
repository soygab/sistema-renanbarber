from datetime import timedelta
from decimal import Decimal

from django.db.models import Avg, Sum
from django.shortcuts import render
from django.utils import timezone

from apps.agendamentos.models import Appointment
from apps.usuarios.models import User
from utils.permissions import barber_required, client_required


@client_required
def client_home(request):
    today = timezone.localdate()
    appointments = Appointment.objects.filter(client=request.user).select_related("service", "barber")
    next_appointment = appointments.filter(status=Appointment.Status.SCHEDULED, date__gte=today).first()
    recent = appointments.filter(status=Appointment.Status.COMPLETED).order_by("-date", "-start_time")[:4]
    return render(request, "cliente-home.html", {"next_appointment": next_appointment, "recent": recent})


@barber_required
def barber_home(request):
    today = timezone.localdate()
    selected_period = request.GET.get("periodo", "30")
    selected_barber = request.GET.get("barbeiro", "")
    completed = Appointment.objects.filter(status=Appointment.Status.COMPLETED)
    if selected_period in {"1", "7", "30"}:
        completed = completed.filter(date__gte=today - timedelta(days=int(selected_period) - 1))
    if selected_barber.isdigit():
        completed = completed.filter(barber_id=selected_barber)
    total_revenue = completed.aggregate(total=Sum("total_price"))["total"] or Decimal("0")
    today_records = Appointment.objects.filter(date=today, status=Appointment.Status.COMPLETED)
    scheduled_records = Appointment.objects.filter(date=today, status=Appointment.Status.SCHEDULED)
    if selected_barber.isdigit():
        today_records = today_records.filter(barber_id=selected_barber)
        scheduled_records = scheduled_records.filter(barber_id=selected_barber)
    today_revenue = today_records.aggregate(total=Sum("total_price"))["total"] or Decimal("0")
    scheduled_today = scheduled_records.count()

    performance = []
    barbers = User.objects.filter(role=User.Role.BARBER, is_active=True).order_by("first_name")
    visible_barbers = barbers.filter(pk=selected_barber) if selected_barber.isdigit() else barbers
    for barber in visible_barbers:
        records = completed.filter(barber=barber)
        revenue = records.aggregate(total=Sum("total_price"))["total"] or Decimal("0")
        performance.append({
            "barber": barber,
            "appointments": records.count(),
            "revenue": revenue,
            "rating": records.aggregate(value=Avg("rating"))["value"],
            "commission": revenue * barber.commission_rate / Decimal("100"),
        })
    pending_commissions = sum((item["commission"] for item in performance), Decimal("0"))
    recent_activity = Appointment.objects.filter(status__in=[Appointment.Status.SCHEDULED, Appointment.Status.COMPLETED]).select_related("client", "barber", "service")
    if selected_barber.isdigit():
        recent_activity = recent_activity.filter(barber_id=selected_barber)
    recent_activity = recent_activity.order_by("-updated_at")[:7]
    return render(request, "barbeiro-home.html", {
        "total_revenue": total_revenue,
        "today_revenue": today_revenue,
        "scheduled_today": scheduled_today,
        "pending_commissions": pending_commissions,
        "performance": performance,
        "recent_activity": recent_activity,
        "barbers": barbers,
        "selected_period": selected_period,
        "selected_barber": selected_barber,
    })
