from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from ..forms.producto_form import ProductoForm
from ..models import Producto


def lista_productos(request):
    productos = Producto.objects.all().order_by('id')
    paginador = Paginator(productos, 10)

    pagina = request.GET.get('page')
    productos_paginados = paginador.get_page(pagina)

    return render(
        request,
        "producto/lista.html",
        context={'productos': productos_paginados},
    )


def delete_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if producto.imagen:
        producto.imagen.storage.delete(producto.imagen.name)
    producto.delete()
    return redirect('list_producto')


def add_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_producto')
        else:
            return render(request, "producto/add.html", context={'form': form})
    return render(
        request, "producto/add.html", context={'form': ProductoForm()}
    )


def update_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.update(producto)
            return redirect('list_producto')
        else:
            return render(
                request, "producto/update.html", context={'form': form}
            )

    form = ProductoForm(
        initial={
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio_compra': producto.precio_compra,
            'precio_venta': producto.precio_venta,
            'stock': producto.stock,
            'categoria': producto.categoria,
            'imagen': producto.imagen,
        }
    )
    return render(
        request,
        "producto/update.html",
        context={'form': form, 'producto': producto},
    )

