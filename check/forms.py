from django import forms
from .models import Checklist

class ChecklistForm(forms.ModelForm):
    data_entrega = forms.DateField(
        input_formats=['%Y-%m-%d'],  
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Checklist
        fields = ['titulo', 'disciplina', 'data_entrega', 'prioridade']
