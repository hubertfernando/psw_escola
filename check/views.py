from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Checklist
from .forms import ChecklistForm

@login_required
def checklist_lista(request):
    """Lista todas as checklists do usuário atual"""
    object_list = Checklist.objects.filter(usuario=request.user)
    return render(request, 'check/index.html', {
        'object_list': object_list
    })

@login_required
def checklist_criar(request):
    """Cria uma nova checklist"""
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.usuario = request.user  # Associa ao usuário logado
            checklist.save()
            messages.success(request, 'Checklist criada com sucesso!')
            return redirect('checklist_lista')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ChecklistForm()
    
    return render(request, 'check/cria.html', {
        'form': form
    })

@login_required
def checklist_editar(request, pk):
    """Edita uma checklist existente"""
    checklist = get_object_or_404(Checklist, pk=pk)
    
    # Verifica se o usuário tem permissão para editar
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar esta checklist.")
    
    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Checklist atualizada com sucesso!')
            return redirect('checklist_lista')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ChecklistForm(instance=checklist)

    return render(request, 'check/atualiza.html', {
        'form': form,
        'checklist': checklist
    })

@login_required
def checklist_detalhe(request, pk):
    """Exibe os detalhes de uma checklist"""
    checklist = get_object_or_404(Checklist, pk=pk)
    
    # Verifica permissão
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para visualizar esta checklist.")
    
    return render(request, 'check/detalhe.html', {
        'checklist': checklist
    })

@login_required
def checklist_deletar(request, pk):
    """Deleta uma checklist"""
    checklist = get_object_or_404(Checklist, pk=pk)
    
    # Verifica permissão
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para deletar esta checklist.")
    
    if request.method == 'POST':
        checklist.delete()
        messages.success(request, 'Checklist deletada com sucesso!')
        return redirect('checklist_lista')

    return render(request, 'check/deleta.html', {
        'checklist': checklist
    })

def checklist_cancelar(request):
    """Redireciona para a lista de checklists"""
    return redirect('checklist_lista')

@login_required
def checklist_alternar(request, pk):
    """Alterna o status de conclusão de uma checklist"""
    checklist = get_object_or_404(Checklist, pk=pk)
    
    # Verifica permissão
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para modificar esta checklist.")
    
    checklist.alternar_status()
    
    status = "concluída" if checklist.concluido else "pendente"
    messages.success(request, f'Checklist marcada como {status}!')
    
    return redirect('checklist_lista')