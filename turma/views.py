from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Turma
from .forms import TurmaForm


# view que lista

def index(request):
    
    turmas = Turma.objects.all()

    return render(request, 'turma/index.html', {'turmas': turmas})

# view que detalha

def detalhe(request, id_turma):

    turma = Turma.objects.get(id=id_turma)

    return render(request, 'turma/detalhe.html', {'turma': turma})

# view que cria

def cria(request):

    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/turma/")

    else:
        form = TurmaForm()

    return render(request, 'turma/cria.html', {'form': form})

# view que atualiza

def atualiza(request, id_turma):
    # recuperando a turma que será atualizada
    turma = Turma.objects.get(pk=id_turma)

    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/turma/")
    else:
        form = TurmaForm(instance=turma)

    return render(request, 'turma/atualiza.html', {'form': form})

# view que apaga

def deleta(request, id_turma):

    turma = Turma.objects.get(id=id_turma)
    turma.delete()

    return HttpResponseRedirect('/turma/')
