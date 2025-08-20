from django.shortcuts import render, redirect, get_object_or_404
from .models import Checklist
from .forms import ChecklistForm


def checklist_lista(request):
    object_list = Checklist.objects.all()
    return render(request, 'atividade/index.html', {
      'object_list': object_list
    })

def checklist_criar(request):
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checklist_lista')
        else:
            print(form.errors)
    else:
        form = ChecklistForm()

    return render(request, 'atividade/cria.html', {
        'form': form
    })



def checklist_editar(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)

    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            return redirect('checklist_lista')
    else:
        form = ChecklistForm(instance=checklist)

    return render(request, 'atividade/atualiza.html', {
        'form': form,
        'checklist': checklist
    })



def checklist_detalhe(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    return render(request, 'atividade/detalhe.html', {
        'checklist': checklist
    })



def checklist_deletar(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    if request.method == 'POST':
        checklist.delete()
        return redirect('checklist_lista')

    return render(request, 'atividade/deleta.html', {
        'checklist': checklist
    })



def checklist_cancelar(request):
    return redirect('checklist_lista')



def checklist_alternar(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    checklist.alternar_status()
    return redirect('checklist_lista')
