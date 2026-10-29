from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from ..forms.cliente_forms import ClienteForm
from ..models import Cliente


@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('id')
    paginador = Paginator(clientes, 10)

    pagina = request.GET.get('page')
    clientes_paginados = paginador.get_page(pagina)

    return render(
        request,
        "cliente/lista.html",
        context={'clientes': clientes_paginados},
    )


@login_required
def add_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_cliente")
    else:
        form = ClienteForm()

    return render(request, "cliente/add.html", context={"form": form})


@login_required
def update_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.update(cliente)
            return redirect("list_cliente")
    else:
        form = ClienteForm(
            initial={
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "telefono": cliente.telefono,
                "correo": cliente.correo,
                "direccion": cliente.direccion,
            }
        )

    return render(
        request,
        "cliente/update.html",
        context={"form": form, "cliente": cliente},
    )


@login_required
def delete_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect("list_cliente")

