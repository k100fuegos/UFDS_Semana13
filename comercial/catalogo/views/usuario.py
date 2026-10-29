from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from ..forms.usuario_forms import UsuarioCreateAdminForm, UsuarioUpdateAdminForm
from ..models import Usuario


def _es_admin(user):
    return user.is_authenticated and hasattr(user, 'rol') and user.rol and user.rol.nombre == 'admin'


@login_required
def lista_usuarios(request):
    if not _es_admin(request.user):
        messages.error(request, "Acceso restringido a administradores.")
        return redirect('home')

    usuarios = Usuario.objects.select_related('rol').all().order_by('id')
    paginador = Paginator(usuarios, 10)

    pagina = request.GET.get('page')
    usuarios_paginados = paginador.get_page(pagina)

    return render(
        request,
        "usuario/lista.html",
        context={'usuarios': usuarios_paginados},
    )


@login_required
def add_usuario(request):
    if not _es_admin(request.user):
        messages.error(request, "Acceso restringido a administradores.")
        return redirect('home')

    if request.method == "POST":
        form = UsuarioCreateAdminForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            messages.success(
                request, f"Usuario '{nuevo_usuario.username}' creado con éxito."
            )
            return redirect("list_usuario")
    else:
        form = UsuarioCreateAdminForm()

    return render(request, "usuario/add.html", context={"form": form})


@login_required
def update_usuario(request, id):
    if not _es_admin(request.user):
        messages.error(request, "Acceso restringido a administradores.")
        return redirect('home')

    usuario = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        form = UsuarioUpdateAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Usuario '{usuario.username}' actualizado."
            )
            return redirect("list_usuario")
    else:
        form = UsuarioUpdateAdminForm(instance=usuario)

    return render(
        request,
        "usuario/update.html",
        context={"form": form, "usuario": usuario},
    )


@login_required
def delete_usuario(request, id):
    if not _es_admin(request.user):
        messages.error(request, "Acceso restringido a administradores.")
        return redirect('home')

    usuario = get_object_or_404(Usuario, id=id)

    if usuario.id == request.user.id:
        messages.error(request, "No puede eliminar su propia cuenta de administrador.")
        return redirect("list_usuario")

    usuario.delete()
    messages.success(request, f"Usuario '{usuario.username}' eliminado.")
    return redirect("list_usuario")

