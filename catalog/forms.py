from django import forms

from .models import ProviderProfile, Service


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ('business_name', 'description', 'zone', 'schedule', 'phone')
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('service_type', 'title', 'description', 'reference_price', 'is_active')
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

    def clean_reference_price(self):
        price = self.cleaned_data['reference_price']
        if price < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return price


class SearchForm(forms.Form):
    service_type = forms.ChoiceField(
        label='Tipo', required=False, choices=[('', 'Todos los servicios')] + Service.Type.choices
    )
    zone = forms.CharField(label='Zona', required=False)
    min_price = forms.DecimalField(label='Precio mín.', required=False, min_value=0)
    max_price = forms.DecimalField(label='Precio máx.', required=False, min_value=0)
