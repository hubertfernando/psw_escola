from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Disciplina
from .forms import DisciplinaForm
from django.contrib.auth.decorators import login_required, permission_required
from turma.models import Turma

@login_required
def index(request):
    turma_id = request.GET.get('turma')
    if not turma_id:
        # Redireciona para lista de turmas
        return HttpResponseRedirect('/turma/')
    turma = get_object_or_404(Turma, id=turma_id)
    disciplinas = Disciplina.objects.filter(turma=turma)
    return render(request, 'disciplina/index.html', {
        'disciplinas': disciplinas,
        'turma': turma,
    })


@login_required
def disciplinas_da_turma(request, id_turma):
    turma = get_object_or_404(Turma, id=id_turma)
    disciplinas = Disciplina.objects.filter(turma=turma)
    return render(request, 'disciplina/index.html', {
        'disciplinas': disciplinas,
        'turma': turma,
    })

@login_required
def detalha(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id=id_disciplina)
    return render(request, 'disciplina/detalha.html', {'disciplina': disciplina})

@login_required
@permission_required('disciplina.add_disciplina', raise_exception=True)
def cria(request):
    turma_id = request.GET.get('turma')
    if not turma_id:
        # Se não tem turma, redireciona para lista de turmas (ou outra página adequada)
        return HttpResponseRedirect('/turma/')

    turma = get_object_or_404(Turma, id=turma_id)

    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save(commit=False)
            disciplina.turma = turma  # fixa turma associada
            disciplina.save()
            return HttpResponseRedirect(f'/disciplina/?turma={turma.id}')
    else:
        form = DisciplinaForm()

    return render(request, 'disciplina/cria.html', {'form': form, 'turma': turma})

@login_required
@permission_required('disciplina.change_disciplina', raise_exception=True)
def atualiza(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id=id_disciplina)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/disciplina/?turma={disciplina.turma.id}')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'disciplina/atualiza.html', {'form': form})

@login_required
@permission_required('disciplina.delete_disciplina', raise_exception=True)
def delete(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id=id_disciplina)
    turma_id = disciplina.turma.id if disciplina.turma else None
    disciplina.delete()
    if turma_id:
        return HttpResponseRedirect(f'/disciplina/?turma={turma_id}')
    return HttpResponseRedirect('/disciplina/')
