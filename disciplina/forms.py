from .models import Disciplina
from django.forms import ModelForm

# Formulário para criar uma nova disciplina
class DisciplinaForm(ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome']
        