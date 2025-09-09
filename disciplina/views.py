from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Disciplina
from .forms import DisciplinaForm
from turma.models import Turma  

@login_required
def index(request):
    turma_id = request.GET.get('turma')
    if not turma_id:
        return HttpResponseRedirect('/turma/')
    
    turma = get_object_or_404(Turma, id=turma_id)
    disciplinas = Disciplina.objects.filter(turma=turma)
    
    return render(request, 'disciplina/index.html', {
        'disciplinas': disciplinas,
        'turma': turma,
        'is_lider': turma.lider == request.user  # Para usar no template
    })

@login_required
def disciplinas_da_turma(request, id_turma):
    turma = get_object_or_404(Turma, id=id_turma)
    disciplinas = Disciplina.objects.filter(turma=turma)
    
    return render(request, 'disciplina/index.html', {
        'disciplinas': disciplinas,
        'turma': turma,
        'is_lider': turma.lider == request.user
    })

@login_required
def detalha(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id=id_disciplina)
    
    # Verifica se usuário tem acesso à disciplina (é líder ou pertence à turma)
    if not (disciplina.turma.lider == request.user or request.user in disciplina.turma.membros.all()):
        return HttpResponseForbidden("Acesso negado")
    
    return render(request, 'disciplina/detalha.html', {'disciplina': disciplina})

@login_required
def cria(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)

    # Verificação do líder
    if not turma.lider or turma.lider != request.user:
        messages.error(request, "Apenas o líder da turma pode criar disciplinas.")
        return HttpResponseRedirect(f'/disciplina/?turma={turma.id}')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save(commit=False)
            disciplina.turma = turma
            disciplina.save()
            messages.success(request, "Disciplina criada com sucesso!")
            return HttpResponseRedirect(f'/disciplina/?turma={turma.id}')
    else:
        form = DisciplinaForm()

    return render(request, 'disciplina/cria.html', {
        'form': form, 
        'turma': turma
    })

@login_required
def atualiza(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id=id_disciplina)
    
    # Verifica se o usuário é o líder da turma
    if disciplina.turma.lider != request.user:
        messages.error(request, "Apenas o líder da turma pode editar disciplinas.")
        return HttpResponseRedirect(f'/disciplina/?turma={disciplina.turma.id}')

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, "Disciplina atualizada com sucesso!")
            return HttpResponseRedirect(f'/disciplina/?turma={disciplina.turma.id}')
        else:
            messages.error(request, "Erro ao atualizar disciplina.")
    else:
        form = DisciplinaForm(instance=disciplina)
    
    return render(request, 'disciplina/atualiza.html', {'form': form})

@login_required
def delete(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id=id_disciplina)
    
    # Verifica se o usuário é o líder da turma
    if disciplina.turma.lider != request.user:
        messages.error(request, "Apenas o líder da turma pode excluir disciplinas.")
        return HttpResponseRedirect(f'/disciplina/?turma={disciplina.turma.id}')

    turma_id = disciplina.turma.id
    disciplina.delete()
    messages.success(request, "Disciplina excluída com sucesso!")
    return HttpResponseRedirect(f'/disciplina/?turma={turma_id}')

def landing_page(request):
    return render(request, 'disciplina/landing.html')