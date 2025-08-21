from django import forms
from .models import Checklist

class ChecklistForm(forms.ModelForm):
    data_entrega = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d']
    )
    
    class Meta:
        model = Checklist
        # NÃO inclua 'usuario' aqui - ele será definido automaticamente na view
        fields = ['titulo', 'descricao', 'disciplina', 'data_entrega', 'prioridade']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
            'prioridade': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título da Atividade',
            'descricao': 'Descrição',
            'disciplina': 'Disciplina',
            'data_entrega': 'Data de Entrega', 
            'prioridade': 'Nível de Prioridade',
        }
    
    # Adicione validação personalizada se necessário
    def clean_data_entrega(self):
        data = self.cleaned_data.get('data_entrega')
        from django.utils import timezone
        if data and data < timezone.now().date():
            raise forms.ValidationError("A data de entrega não pode ser no passado.")
        return data