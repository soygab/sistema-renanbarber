from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from utils.permissions import barber_required, client_required

from .forms import ServiceForm
from .models import Service


@client_required
def service_list(request):
    return render(request, "servicos.html", {"services": Service.objects.filter(active=True)})


@barber_required
def service_manage(request, pk=None):
    service = get_object_or_404(Service, pk=pk) if pk else None
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Serviço salvo com sucesso.")
        return redirect("service_manage")
    return render(request, "barbeiro-servicos.html", {
        "services": Service.objects.filter(active=True),
        "form": form,
        "editing": service,
    })


@require_POST
@barber_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if service.appointments.exists():
        service.active = False
        service.save(update_fields=["active", "updated_at"])
        messages.success(request, "Serviço arquivado. O histórico dos agendamentos foi preservado.")
    else:
        service.delete()
        messages.success(request, "Serviço excluído com sucesso.")
    return redirect("service_manage")
