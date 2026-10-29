from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from ..forms.categoria_forms import CategoriaForm
from ..models.categoria import Categoria


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(
        request, "categoria/lista.html", context={'categorias': categorias}
    )


@login_required
def delete_categoria(request, id):
    if request.method != "POST":
        return redirect("list_categoria")

    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect("list_categoria")


@login_required
def add_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_categoria")
    else:
        form = CategoriaForm()

    return render(request, "categoria/add.html", context={"form": form})


@login_required
def update_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.update(categoria)
            return redirect("list_categoria")
    else:
        form = CategoriaForm(
            initial={
                "nombre": categoria.nombre,
                "descripcion": categoria.descripcion,
            }
        )

    return render(
        request,
        "categoria/update.html",
        context={"form": form, "categoria": categoria},
    )
