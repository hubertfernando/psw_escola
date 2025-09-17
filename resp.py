from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Aluno
from .forms import AlunoForm, AlunoEditForm

@login_required
def index(request):
    alunos = Aluno.objects.all()
    return render(request, 'aluno/index.html', {'alunos': alunos})

@login_required
@permission_required('disciplina.add_disciplina')
def detalha(request, id_aluno):
    aluno = get_object_or_404(Aluno, id=id_aluno)
    return render(request, 'aluno/detalha.html', {'aluno': aluno})

def cria(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/aluno/")
    else:
        form = AlunoForm()
    return render(request, 'aluno/cria.html', {'form': form})

@login_required
def atualiza(request, id_aluno):
    aluno = get_object_or_404(Aluno, id=id_aluno)

    if request.method == 'POST':
        form = AlunoEditForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, "Aluno atualizado com sucesso!")
            return redirect('index-aluno')
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = AlunoEditForm(instance=aluno)

    return render(request, 'aluno/atualiza.html', {
        'form': form,
    })

@login_required
@permission_required('')
@test_passed_groups('Admin')
def delete(request, id_aluno):
    aluno = get_object_or_404(Aluno, id=id_aluno)
    aluno.delete()  
    return HttpResponseRedirect("/aluno/")

