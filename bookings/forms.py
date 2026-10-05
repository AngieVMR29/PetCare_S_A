from django import forms
from django.utils import timezone

from .models import BookingRequest


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ('pet_name', 'pet_species', 'date', 'time', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise forms.ValidationError('La fecha no puede ser pasada.')
        return date


class RejectForm(forms.Form):
    reason = forms.CharField(label='Motivo (opcional)', required=False, max_length=255)
