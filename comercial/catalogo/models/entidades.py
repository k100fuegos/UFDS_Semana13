from django.conf import settings
from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    # Django ya gestiona username, contraseña, nombre, apellido y correo.
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    rol = models.ForeignKey("Rol", on_delete=models.PROTECT)
    telefono = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(
        max_length=255, blank=True, null=True, verbose_name="Descripción")
    precio_compra = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio de Compra")
    precio_venta = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    imagen = models.ImageField(
        upload_to='productos/', blank=True, null=True, verbose_name="Imagen")
    categoria = models.ForeignKey(
        "Categoria", on_delete=models.PROTECT, related_name="productos", verbose_name="Categoría")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return f"id: {self.id} Nombre: {self.nombre} Precio de compra: {self.precio_compra} Precio de venta: {self.precio_venta}, Stock: {self.stock}"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TipoPago(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey("Cliente", on_delete=models.PROTECT)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    tipo_pago = models.ForeignKey("TipoPago", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        "Venta",
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    producto = models.ForeignKey("Producto", on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
