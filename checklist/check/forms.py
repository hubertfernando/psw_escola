from django import forms
from .models import Checklist

# Criamos um ModelForm que já se baseia no modelo Checklist
class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist  # Indicamos que o formulário será do modelo Checklist
        fields = ['titulo', 'disciplina', 'data_entrega', 'concluido', 'prioridade']
        widgets = {
    'data_entrega': forms.DateInput(attrs={'type': 'date'})
}
