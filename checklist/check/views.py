from django.shortcuts import render, redirect, get_object_or_404
from .models import Checklist
from .forms import ChecklistForm
from django.views.decorators.csrf import csrf_exempt

def checklist_base(request, pk=None):
    if pk:
        checklist = get_object_or_404(Checklist, pk=pk)
        form = ChecklistForm(instance=checklist)
    else:
        form = ChecklistForm()

    if request.method == 'POST':
        if pk:
            form = ChecklistForm(request.POST, instance=checklist)
        else:
            form = ChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checklist_list')

    checklists = Checklist.objects.all()
    return render(request, 'base.html', {'checklists': checklists, 'form': form})

def checklist_delete_inline(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    if request.method == 'POST':
        checklist.delete()
    return redirect('checklist_list')

def checklist_clear_form(request):
    return redirect('checklist_list')

def checklist_toggle(request, pk):
    checklist = get_object_or_404(Checklist, pk=pk)
    checklist.alternar_status()
    return redirect('checklist_list')


