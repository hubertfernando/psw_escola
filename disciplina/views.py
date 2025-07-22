from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Disciplina
from .forms import DisciplinaForm
from django.contrib.auth.decorators import login_required, permission_required

# View que lista todas as disciplinas (pode ser ajustada futuramente para listar apenas as do aluno)
@login_required
def index(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'disciplina/index.html', {'disciplinas': disciplinas})


# View para detalhar uma disciplina
@login_required
def detalha(request, id_disciplina):
    disciplina = Disciplina.objects.get(id=id_disciplina)
    return render(request, 'disciplina/detalha.html', {'disciplina': disciplina})


# View que create novas disciplinas
@login_required
@permission_required('disciplina.add_categoria', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/disciplina/")
    else:
        form = CategoriaForm()
    return render(request, 'disciplina/create.html', {'form': form})


# View que edita uma disciplina
@login_required
@permission_required('disciplina.change_categoria', raise_exception=True)
def atualiza(request, id_disciplina):
    disciplina = Disciplina.objects.get(id=id_disciplina)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/disciplina/")
    else:
        form = CategoriaForm(instance=disciplina)
    return render(request, 'disciplina/atualiza.html', {'form': form})


# View que deleta uma disciplina
@login_required
@permission_required('disciplina.delete_categoria', raise_exception=True)
def delete(request, id_disciplina):
    disciplina = Disciplina.objects.get(id=id_disciplina)
    disciplina.delete()
    return HttpResponseRedirect("/disciplina/")