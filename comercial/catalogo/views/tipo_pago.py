from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from ..forms.tipo_pago_forms import TipoPagoForm
from ..models import TipoPago


@login_required
def lista_tipo_pago(request):
    tipos_pago = TipoPago.objects.all().order_by('id')
    paginador = Paginator(tipos_pago, 10)

    pagina = request.GET.get('page')
    tipos_pago_paginados = paginador.get_page(pagina)

    return render(
        request,
        "tipo_pago/lista.html",
        context={'tipos_pago': tipos_pago_paginados},
    )


@login_required
def add_tipo_pago(request):
    if request.method == "POST":
        form = TipoPagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_tipo_pago")
    else:
        form = TipoPagoForm()

    return render(request, "tipo_pago/add.html", context={"form": form})


@login_required
def update_tipo_pago(request, id):
    tipo_pago = get_object_or_404(TipoPago, id=id)

    if request.method == "POST":
        form = TipoPagoForm(request.POST)
        if form.is_valid():
            form.update(tipo_pago)
            return redirect("list_tipo_pago")
    else:
        form = TipoPagoForm(
            initial={
                "nombre": tipo_pago.nombre,
                "descripcion": tipo_pago.descripcion,
            }
        )

    return render(
        request,
        "tipo_pago/update.html",
        context={"form": form, "tipo_pago": tipo_pago},
    )


@login_required
def delete_tipo_pago(request, id):
    tipo_pago = get_object_or_404(TipoPago, id=id)
    tipo_pago.delete()
    return redirect("list_tipo_pago")

