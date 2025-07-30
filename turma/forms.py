from .models import Turma
from django.forms import ModelForm


class TurmaForm(ModelForm):
    class Meta: 
        model = Turma
        fields = ['curso', 'ano', 'lider']
