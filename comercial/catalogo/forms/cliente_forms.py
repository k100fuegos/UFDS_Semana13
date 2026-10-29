from django import forms
from ..models import Cliente


class ClienteForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre", required=True)
    apellido = forms.CharField(max_length=100, label="Apellido", required=True)
    telefono = forms.CharField(max_length=9, label="Teléfono", required=True)
    correo = forms.EmailField(label="Correo Electrónico", required=False)
    direccion = forms.CharField(
        max_length=255,
        label="Dirección",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    def save(self):
        if not self.is_valid():
            raise ValueError(
                "No se puede guardar un cliente con datos inválidos."
            )

        return Cliente.objects.create(
            nombre=self.cleaned_data["nombre"],
            apellido=self.cleaned_data["apellido"],
            telefono=self.cleaned_data["telefono"],
            correo=self.cleaned_data.get("correo") or None,
            direccion=self.cleaned_data.get("direccion") or None,
        )

    def update(self, cliente):
        if not self.is_valid():
            raise ValueError(
                "No se puede actualizar un cliente con datos inválidos."
            )

        cliente.nombre = self.cleaned_data["nombre"]
        cliente.apellido = self.cleaned_data["apellido"]
        cliente.telefono = self.cleaned_data["telefono"]
        cliente.correo = self.cleaned_data.get("correo") or None
        cliente.direccion = self.cleaned_data.get("direccion") or None
        cliente.save()
        return cliente

