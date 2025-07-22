from .models import Aluno
from django.forms import ModelForm

# Importando o django.contrib.auth.forms com os formulários prontos para a criação e edição de alunos
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class AlunoForm(UserCreationForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'telefone', 'matricula', 'turma']

class AlunoEditForm(UserChangeForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'telefone', 'matricula', 'turma']
        