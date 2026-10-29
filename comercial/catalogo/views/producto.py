from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from ..forms.producto_form import ProductoForm
from ..models import Producto


@login_required
def lista_productos(request):
    usuario = request.user
    if usuario.rol.nombre != 'admin':
        return redirect('home')

    productos = Producto.objects.all().order_by('id')
    paginador = Paginator(productos, 10)

    pagina = request.GET.get('page')
    productos_paginados = paginador.get_page(pagina)

    return render(
        request,
        "producto/lista.html",
        context={'productos': productos_paginados},
    )


@login_required
def delete_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if producto.imagen:
        producto.imagen.storage.delete(producto.imagen.name)
    producto.delete()
    return redirect('list_producto')


@login_required
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


@login_required
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


@login_required
def generar_pdf_view(request):
    try:
        from weasyprint import HTML

        productos = Producto.objects.all()
        contexto = {'productos': productos}
        html_string = render_to_string('producto/reporte.html', contexto)
        pdf = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="documento.ico.pdf"'
        return response
    except Exception as e:
        return HttpResponse(
            f"Error al generar PDF con WeasyPrint: {e}. "
            "Asegúrese de haber instalado las dependencias GTK/Pango en Windows conforme la guía de la semana 14.",
            status=500,
        )
