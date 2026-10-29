from django.urls import path
from .views.categoria import (
    add_categoria,
    delete_categoria,
    lista_categorias,
    update_categoria,
)

urlpatterns = [
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
]
