from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Aluno

class AlunoCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=100)
    matricula = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nome', 'telefone', 'matricula']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Aluno.objects.create(
                user=user,
                nome=self.cleaned_data['nome'],
                telefone=self.cleaned_data['telefone'],
                matricula=self.cleaned_data['matricula'],
            )
        return user

class UsuarioEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)  # Remove o campo de senha

class AlunoEditForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'telefone', 'matricula']