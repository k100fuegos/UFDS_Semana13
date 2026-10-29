from django import forms
from ..models import TipoPago


class TipoPagoForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre", required=True)
    descripcion = forms.CharField(
        max_length=255,
        label="Descripción",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    def save(self):
        if not self.is_valid():
            raise ValueError(
                "No se puede guardar un tipo de pago con datos inválidos."
            )

        return TipoPago.objects.create(
            nombre=self.cleaned_data["nombre"],
            descripcion=self.cleaned_data.get("descripcion") or None,
        )

    def update(self, tipo_pago):
        if not self.is_valid():
            raise ValueError(
                "No se puede actualizar un tipo de pago con datos inválidos."
            )

        tipo_pago.nombre = self.cleaned_data["nombre"]
        tipo_pago.descripcion = self.cleaned_data.get("descripcion") or None
        tipo_pago.save()
        return tipo_pago

