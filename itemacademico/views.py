from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ItemAcademico, Atividade, Material
from .forms import ItemAcademicoForm, AtividadeForm, MaterialForm
from disciplina.models import Disciplina  
from django.http import HttpResponseRedirect


# Página inicial: lista separada de atividades e materiais (todos os itens)
@login_required
def index(request):
    disciplina_id = request.GET.get('disciplina')
    if not disciplina_id:
        # Redireciona para lista de turmas ou disciplinas
        return HttpResponseRedirect('/disciplina/')
    
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    atividades = Atividade.objects.filter(disciplina=disciplina).order_by('-data_criacao')
    materiais = Material.objects.filter(disciplina=disciplina).order_by('-data_criacao')

    return render(request, 'itemacademico/index.html', {
        'disciplina': disciplina,
        'atividades': atividades,
        'materiais': materiais
    })

# Listar itens acadêmicos filtrados por disciplina
@login_required
def itens_por_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    atividades = Atividade.objects.filter(disciplina=disciplina).order_by('-data_criacao')
    materiais = Material.objects.filter(disciplina=disciplina).order_by('-data_criacao')
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

# Criação de atividade ou material, associando disciplina
@login_required
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
        elif tipo == 'MATERIAL':
            form = MaterialForm(request.POST, request.FILES)
        else:
            form = ItemAcademicoForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.tipo = tipo
            if disciplina:
                item.disciplina = disciplina
            item.save()
            if disciplina:
                return redirect('itemacademico:itens_por_disciplina', disciplina_id=disciplina.id)
            else:
                return redirect('itemacademico:index')
    else:
        if tipo == 'ATIVIDADE':
            form = AtividadeForm(initial={'tipo': 'ATIVIDADE'})
        elif tipo == 'MATERIAL':
            form = MaterialForm(initial={'tipo': 'MATERIAL'})
        else:
            form = ItemAcademicoForm()

    return render(request, 'itemacademico/cria.html', {
        'form': form,
        'tipo_selecionado': tipo,
        'disciplina': disciplina,
    })

# Atualização de atividade ou material
@login_required
def atualiza(request, id_itemacademico):
    item_academico_pai = get_object_or_404(ItemAcademico, pk=id_itemacademico)

    instance = None
    FormClass = None

    try:
        instance = item_academico_pai.atividade
        FormClass = AtividadeForm
    except Atividade.DoesNotExist:
        try:
            instance = item_academico_pai.material
            FormClass = MaterialForm
        except Material.DoesNotExist:
            instance = item_academico_pai
            FormClass = ItemAcademicoForm

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            # Redirecionar para a lista da disciplina do item atualizado, se houver
            disciplina = instance.disciplina if hasattr(instance, 'disciplina') else None
            if disciplina:
                return redirect('itemacademico:itens_por_disciplina', disciplina_id=disciplina.id)
            return redirect('itemacademico:index')
    else:
        form = FormClass(instance=instance)

    return render(request, 'itemacademico/atualiza.html', {'form': form, 'item': instance})

@login_required
def deleta(request, id_itemacademico):
    item = get_object_or_404(ItemAcademico, id=id_itemacademico)
    disciplina = item.disciplina if hasattr(item, 'disciplina') else None
    item.delete()
    if disciplina:
        return redirect('itemacademico:itens_por_disciplina', disciplina_id=disciplina.id)
    return redirect('itemacademico:index')
