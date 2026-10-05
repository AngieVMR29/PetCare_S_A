from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """HU-01: registro con nombre, correo, contraseña (mín. 8) y rol."""

    ROLE_CHOICES = [(User.Role.OWNER, 'Propietario de mascota'), (User.Role.PROVIDER, 'Proveedor de servicios')]

    first_name = forms.CharField(label='Nombre', max_length=150)
    email = forms.EmailField(label='Correo electrónico')
    role = forms.ChoiceField(label='Soy', choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'role')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # el correo es el identificador de acceso
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Correo electrónico')
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Correo o contraseña incorrectos.',  # no revela cuál falló (HU-02)
    }

    def clean_username(self):
        return self.cleaned_data['username'].lower()
