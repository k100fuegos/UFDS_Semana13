from django.contrib.auth import login
from django.shortcuts import redirect, render
from ..forms.registrarUser_form import RegistrarUserForm


def registraUsuario(request):
    if request.method == "POST":
        form = RegistrarUserForm(request.POST)
        if form.is_valid():
            form.instance.rol_id = 2
            usuario = form.save()
            login(request, usuario)
            return redirect("home")
    else:
        form = RegistrarUserForm()
    return render(
        request, "registraUsuario/registraUsuario.html", context={"form": form}
    )

