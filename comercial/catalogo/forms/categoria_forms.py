from django import forms
from ..models.categoria import Categoria


class CategoriaForm(forms.Form):
    nombre = forms.CharField(max_length=255, label="Nombre", required=True)
    descripcion = forms.CharField(
        max_length=255,
        label="Descripción",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def save(self):
        if not self.is_valid():
            raise ValueError(
                "No se puede guardar una categoría con datos inválidos.")

        return Categoria.objects.create(
            nombre=self.cleaned_data["nombre"],
            descripcion=self.cleaned_data["descripcion"],
        )

    def update(self, categoria):
        if not self.is_valid():
            raise ValueError(
                "No se puede actualizar una categoría con datos inválidos.")

        categoria.nombre = self.cleaned_data["nombre"]
        categoria.descripcion = self.cleaned_data["descripcion"]
        categoria.save()
        return categoria
