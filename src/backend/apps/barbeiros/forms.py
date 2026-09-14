from django import forms

from .models import BarberAvailability, TimeBlock


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = BarberAvailability
        fields = ("weekday", "start_time", "end_time", "active")
        widgets = {"weekday": forms.HiddenInput(), "start_time": forms.TimeInput(attrs={"type": "time"}), "end_time": forms.TimeInput(attrs={"type": "time"})}


class TimeBlockForm(forms.ModelForm):
    class Meta:
        model = TimeBlock
        fields = ("start", "end", "reason")
        widgets = {
            "start": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "reason": forms.TextInput(attrs={"placeholder": "Ex.: almoço, compromisso"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end"].input_formats = ["%Y-%m-%dT%H:%M"]
