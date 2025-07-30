from .models import Atividade
from django.forms import ModelForm, DateInput

class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao', 'data_entrega', 'arquivo']
        widgets = {
            'data_entrega': DateInput(attrs={'type': 'date'}),
        }
