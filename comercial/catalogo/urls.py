from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views.categoria import (
    add_categoria,
    delete_categoria,
    lista_categorias,
    update_categoria,
)
from .views.cliente import (
    add_cliente,
    delete_cliente,
    lista_clientes,
    update_cliente,
)
from .views.home import home
from .views.inicio import inicio
from .views.producto import (
    add_producto,
    delete_producto,
    generar_pdf_view,
    lista_productos,
    update_producto,
)
from .views.registrarUsuario import registraUsuario
from .views.tipo_pago import (
    add_tipo_pago,
    delete_tipo_pago,
    lista_tipo_pago,
    update_tipo_pago,
)
from .views.usuario import (
    add_usuario,
    delete_usuario,
    lista_usuarios,
    update_usuario,
)
from .views.venta import (
    detalle_venta,
    lista_ventas,
    registrar_venta,
)

urlpatterns = [
    # Inicio y Home
    path("", inicio, name="inicio"),
    path("home/", home, name="home"),
    # Autenticación
    path(
        "login/",
        LoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registrar_usuario/", registraUsuario, name="registrar_usuario"),
    # Categorías
    path("categoria/", lista_categorias, name="list_categoria"),
    path("categoria/agregar/", add_categoria, name="add_categoria"),
    path(
        "categoria/actualizar/<int:id>/",
        update_categoria,
        name="update_categoria",
    ),
    path(
        "categoria/eliminar/<int:id>/",
        delete_categoria,
        name="delete_categoria",
    ),
    # Productos
    path("producto/", lista_productos, name="list_producto"),
    path("producto/agregar/", add_producto, name="add_producto"),
    path(
        "producto/actualizar/<int:id>/",
        update_producto,
        name="update_producto",
    ),
    path(
        "producto/eliminar/<int:id>/",
        delete_producto,
        name="delete_producto",
    ),
    path("reporte_productos/", generar_pdf_view, name="reporte_producto"),
    # Clientes
    path("cliente/", lista_clientes, name="list_cliente"),
    path("cliente/agregar/", add_cliente, name="add_cliente"),
    path(
        "cliente/actualizar/<int:id>/",
        update_cliente,
        name="update_cliente",
    ),
    path(
        "cliente/eliminar/<int:id>/",
        delete_cliente,
        name="delete_cliente",
    ),
    # Tipos de Pago
    path("tipo_pago/", lista_tipo_pago, name="list_tipo_pago"),
    path("tipo_pago/agregar/", add_tipo_pago, name="add_tipo_pago"),
    path(
        "tipo_pago/actualizar/<int:id>/",
        update_tipo_pago,
        name="update_tipo_pago",
    ),
    path(
        "tipo_pago/eliminar/<int:id>/",
        delete_tipo_pago,
        name="delete_tipo_pago",
    ),
    # Ventas
    path("venta/", lista_ventas, name="list_venta"),
    path("venta/registrar/", registrar_venta, name="registrar_venta"),
    path("venta/detalle/<int:id>/", detalle_venta, name="detalle_venta"),
    # Usuarios (Gestión para Administrador)
    path("usuario/", lista_usuarios, name="list_usuario"),
    path("usuario/agregar/", add_usuario, name="add_usuario"),
    path(
        "usuario/actualizar/<int:id>/",
        update_usuario,
        name="update_usuario",
    ),
    path(
        "usuario/eliminar/<int:id>/",
        delete_usuario,
        name="delete_usuario",
    ),
]
