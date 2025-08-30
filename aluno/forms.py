from .models import Aluno
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Formulário para criar um novo usuário, utilizando o UserCreationForm do Django
class AlunoForm(UserCreationForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'telefone', 'matricula']

class AlunoEditForm(UserChangeForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'telefone','matricula']
        