from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import ItemAcademico, Atividade
from .forms import ItemAcademicoForm, AtividadeForm
from disciplina.models import Disciplina

# Página inicial: lista separada de atividades e materiais
@login_required
def index(request):
    disciplina_id = request.GET.get('disciplina')
    if not disciplina_id:
        return HttpResponseRedirect('/disciplina/')
    
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    
    # Atividades continuam como antes
    atividades = Atividade.objects.filter(disciplina=disciplina).order_by('-data_criacao')
    
    # Materiais agora são apenas ItemAcademico com tipo MATERIAL
    materiais = ItemAcademico.objects.filter(disciplina=disciplina, tipo='MATERIAL').order_by('-data_criacao')

    return render(request, 'itemacademico/index.html', {
        'disciplina': disciplina,
        'atividades': atividades,
        'materiais': materiais,
    })

# Listar itens por disciplina
@login_required
def itens_por_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    atividades = Atividade.objects.filter(disciplina=disciplina).order_by('-data_criacao')
    materiais = ItemAcademico.objects.filter(disciplina=disciplina, tipo='MATERIAL').order_by('-data_criacao')
    return render(request, 'itemacademico/index.html', {
        'disciplina': disciplina,
        'atividades': atividades,
        'materiais': materiais,
    })

# Detalhe de um item acadêmico
@login_required
def detalhe(request, id_itemacademico):
    item = get_object_or_404(ItemAcademico, id=id_itemacademico)
    return render(request, 'itemacademico/detalhe.html', {'itemacademico': item})

# Criação de atividade ou material
@login_required
def cria(request, disciplina_id=None):
    disciplina = None
    if disciplina_id:
        disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    else:
        disciplina_id_post = request.POST.get('disciplina')
        if disciplina_id_post:
            disciplina = get_object_or_404(Disciplina, pk=disciplina_id_post)

    tipo = request.POST.get('tipo') if request.method == 'POST' else request.GET.get('tipo')

    if request.method == 'POST':
        if tipo == 'ATIVIDADE':
            form = AtividadeForm(request.POST, request.FILES)
        else:  # MATERIAL ou qualquer outro tipo
            form = ItemAcademicoForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.tipo = tipo
            if disciplina:
                item.disciplina = disciplina
            item.save()
            if disciplina:
                return redirect('itemacademico:itens_por_disciplina', disciplina_id=disciplina.id)
            return redirect('itemacademico:index')
    else:
        if tipo == 'ATIVIDADE':
            form = AtividadeForm(initial={'tipo': 'ATIVIDADE'})
        else:
            form = ItemAcademicoForm(initial={'tipo': 'MATERIAL'})

    return render(request, 'itemacademico/cria.html', {
        'form': form,
        'tipo_selecionado': tipo,
        'disciplina': disciplina,
    })

# Atualização de item acadêmico ou atividade
@login_required
def atualiza(request, id_itemacademico):
    item_academico_pai = get_object_or_404(ItemAcademico, pk=id_itemacademico)

    # Determina se é Atividade ou ItemAcademico
    instance = None
    FormClass = None

    try:
        instance = item_academico_pai.atividade
        FormClass = AtividadeForm
    except Atividade.DoesNotExist:
        instance = item_academico_pai
        FormClass = ItemAcademicoForm

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            disciplina = instance.disciplina if hasattr(instance, 'disciplina') else None
            if disciplina:
                return redirect('itemacademico:itens_por_disciplina', disciplina_id=disciplina.id)
            return redirect('itemacademico:index')
    else:
        form = FormClass(instance=instance)

    return render(request, 'itemacademico/atualiza.html', {'form': form, 'item': instance})

# Deletar item acadêmico
@login_required
def deleta(request, id_itemacademico):
    item = get_object_or_404(ItemAcademico, id=id_itemacademico)
    disciplina = item.disciplina if hasattr(item, 'disciplina') else None
    item.delete()
    if disciplina:
        return redirect('itemacademico:itens_por_disciplina', disciplina_id=disciplina.id)
    return redirect('itemacademico:index')
