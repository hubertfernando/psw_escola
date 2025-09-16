from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from .models import Checklist
from .forms import ChecklistForm
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import date


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
            checklist.usuario = request.user  
            checklist.save()
            return redirect('checklist_lista')
    else:
        form = ChecklistForm()
    
    return render(request, 'check/cria.html', {
        'form': form
    })


@login_required
def checklist_editar(request, pk):
    """Edita uma checklist existente"""
    checklist = get_object_or_404(Checklist, pk=pk)
    
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar esta checklist.")
    
    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            return redirect('checklist_lista')
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
    
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para visualizar esta checklist.")
    
    return render(request, 'check/detalhe.html', {
        'checklist': checklist
    })


@login_required
def checklist_deletar(request, pk):
    """Deleta uma checklist"""
    checklist = get_object_or_404(Checklist, pk=pk)
    
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para deletar esta checklist.")
    
    if request.method == 'POST':
        checklist.delete()
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
    
    if checklist.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para modificar esta checklist.")
    
    checklist.alternar_status()
    
    status = "concluída" if checklist.concluido else "pendente"
    messages.success(request, f'Checklist marcada como {status}!')
    
    return redirect('checklist_lista') 


@login_required
def checklist_calendario(request):
    """Renderiza o calendário com eventos em JSON"""
    qs = Checklist.objects.filter(usuario=request.user)
    events = []

    for obj in qs:
        if obj.prioridade == 5:
            color = "#dc3545"
        elif obj.prioridade == 4:
            color = "#fd7e14"
        elif obj.prioridade == 3:
            color = "#ffc107"
        elif obj.prioridade == 2:
            color = "#0d6efd"
        else:
            color = "#198754"

        events.append({
            "title": obj.titulo,
            "start": obj.data_entrega.strftime("%Y-%m-%d") if obj.data_entrega else None,
            "url": reverse("checklist_detalhe", args=[obj.pk]),
            "color": color,
        })

    return render(request, "check/calendario.html", {
        "events": json.dumps(events, cls=DjangoJSONEncoder)
    })


@require_POST
def checklist_atualiza_data(request, pk):
    """
    Recebe JSON { "date": "YYYY-MM-DD" } quando o usuário arrasta um evento.
    Atualiza o campo data_entrega do Checklist.
    """
    checklist = get_object_or_404(Checklist, pk=pk)

    try:
        data = json.loads(request.body.decode('utf-8'))
        nova_data_str = data.get('date')
        if not nova_data_str:
            return JsonResponse({'status': 'error', 'error': 'campo date ausente'}, status=400)

        nova_data = date.fromisoformat(nova_data_str)
        checklist.data_entrega = nova_data
        checklist.save(update_fields=['data_entrega', 'updated_at'])
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
