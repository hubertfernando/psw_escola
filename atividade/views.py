from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Atividade
from .forms import AtividadeForm

# View que lista todas as atividades (pode ser ajustada futuramente para listar apenas as do aluno)

def index(request):
    atividades = Atividade.objects.all()
    return render(request, 'atividade/index.html', {'atividades': atividades})

# View que detalha uma atividade

def detalhe(request, id_atividade):
    atividade = get_object_or_404(Atividade, id=id_atividade)
    return render(request, 'atividade/detalhe.html', {'atividade': atividade})

# View que cria uma atividade (com upload de arquivo)

def cria(request):
    if request.method == 'POST':
        form = AtividadeForm(request.POST, request.FILES)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.save()
            return HttpResponseRedirect("/atividade/")
    else:
        form = AtividadeForm()

    return render(request, 'atividade/cria.html', {'form': form})

# View que atualiza uma atividade (com upload de arquivo)

def atualiza(request, id_atividade):
    atividade = get_object_or_404(Atividade, pk=id_atividade)

    if request.method == 'POST':
        form = AtividadeForm(request.POST, request.FILES, instance=atividade)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/atividade/")
    else:
        form = AtividadeForm(instance=atividade)

    return render(request, 'atividade/atualiza.html', {'form': form})

# View que deleta uma atividade

def deleta(request, id_atividade):
    atividade = get_object_or_404(Atividade, id=id_atividade)
    atividade.delete()
    return HttpResponseRedirect('/atividade/')
