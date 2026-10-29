from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import Rol, Usuario


class UsuarioCreateAdminForm(UserCreationForm):
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label="Rol",
        empty_label=None,
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefono',
            'rol',
        ]


class UsuarioUpdateAdminForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        label="Rol",
        empty_label=None,
        required=True,
    )

    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'email',
            'telefono',
            'rol',
            'is_active',
        ]
        labels = {
            'is_active': 'Usuario Activo',
        }

