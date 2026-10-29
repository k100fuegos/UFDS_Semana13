from django.contrib.auth.forms import UserCreationForm
from ..models.usuario import Usuario


class RegistrarUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono']

