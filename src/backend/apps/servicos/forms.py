from django import forms

from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("name", "price", "duration_minutes", "description", "active")
        labels = {"name": "Nome", "price": "Preço", "duration_minutes": "Duração (minutos)", "description": "Descrição", "active": "Serviço ativo"}
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
