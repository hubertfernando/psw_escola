from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Aluno
from .forms import AlunoForm, AlunoEditForm
from django.contrib.auth.decorators import login_required, permission_required

# View que lista todos os alunos cadastrados
@login_required
@permission_required('aluno.view_alunos', raise_exception=True)
def index(request):
    alunos = Aluno.objects.all()
    return render(request, 'aluno/index.html', {'alunos': alunos})

# View que mostra os detalhes de um aluno
@login_required
@permission_required('aluno.detail_alunos', raise_exception=True)
def detalha(request, id_alunos):
    aluno = Aluno.objects.get(id=id_alunos) 
    return render(request, 'aluno/detalha.html', {'aluno': aluno})

# View para criar aluno
@login_required
@permission_required('aluno.cria_alunos', raise_exception=True)
def cria(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/aluno/")    
    else:
        form = AlunoForm()
    return render(request, 'aluno/cria.html', {'form': form})

# View para editar alunos
@login_required
@permission_required('aluno.atualiza_alunos', raise_exception=True)
def atualiza(request, id_alunos):
    aluno = Aluno.objects.get(id=id_alunos)
    if request.method == 'POST':
        form = AlunoEditForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/aluno/")    
    else:
        form = AlunoEditForm(instance=aluno)
    return render(request, 'aluno/atualiza.html', {'form': form})

# View para excluir um aluno
@login_required
@permission_required('aluno.delete_aluno', raise_exception=True)
def delete(request, id_aluno):
    Aluno.objects.get(id=id_aluno).delete()
    return HttpResponseRedirect("/aluno/")