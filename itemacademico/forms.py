from django import forms
from .models import ItemAcademico, Atividade

class ItemAcademicoForm(forms.ModelForm):
    class Meta:
        model = ItemAcademico
        fields = ['tipo', 'titulo', 'descricao', 'arquivo']

class AtividadeForm(ItemAcademicoForm):
    class Meta(ItemAcademicoForm.Meta):
        model = Atividade
        fields = ItemAcademicoForm.Meta.fields + ['data_entrega']
        widgets = {
            'data_entrega': forms.DateInput(attrs={'type': 'date'}),
        }
