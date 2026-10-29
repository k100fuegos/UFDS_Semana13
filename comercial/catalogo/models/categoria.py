from django.db import models


class Categoria(models.Model):
    nombre = models.TextField(max_length=255, verbose_name="Nombre")
    descripcion = models.TextField(
        max_length=255, null=True, verbose_name="Descripción")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha de creación")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return f"id: {self.id} Nombre: {self.nombre} Descripcion: {self.descripcion} Fecha de creacion: {self.created_at} Fecha de actualizacion {self.updated_at}"
