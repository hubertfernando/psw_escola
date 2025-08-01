from django.shortcuts import render, get_object_or_404, redirect
from .models import ItemAcademico, Atividade, Material
from .forms import ItemAcademicoForm, AtividadeForm, MaterialForm

# Página inicial: lista separada de atividades e materiais
def index(request):
    atividades = Atividade.objects.all().order_by('-data_criacao')
    materiais = Material.objects.all().order_by('-data_criacao')
    return render(request, 'itemacademico/index.html', {
        'atividades': atividades,
        'materiais': materiais
    })

# Detalhe de um item acadêmico
def detalhe(request, id_itemacademico):
    item = get_object_or_404(ItemAcademico, id=id_itemacademico)
    # Correção: O template esperava 'itemacademico', mas a variável era 'item'
    return render(request, 'itemacademico/detalhe.html', {'itemacademico': item})

# Criação de atividade ou material
def cria(request):
    # Pega o 'tipo' da URL (GET) ou do formulário (POST)
    tipo = request.POST.get('tipo') if request.method == 'POST' else request.GET.get('tipo')

    if request.method == 'POST':
        print("FILES RECEBIDOS:", request.FILES)  # Diagnóstico

        # É importante saber qual instância de modelo usar para o formulário
        # No caso de herança multi-tabela, ao criar, o ModelForm sabe como lidar.
        if tipo == 'ATIVIDADE':
            form = AtividadeForm(request.POST, request.FILES)
        elif tipo == 'MATERIAL':
            form = MaterialForm(request.POST, request.FILES)
        else:
            # Caso não seja ATIVIDADE nem MATERIAL, ou 'tipo' não esteja definido
            # O ideal seria direcionar para uma escolha de tipo ou lançar um erro.
            # Por enquanto, mantemos ItemAcademicoForm, mas ele não tem 'data_entrega'.
            form = ItemAcademicoForm(request.POST, request.FILES)

        if form.is_valid():
            # Quando form.save() é chamado em um ModelForm de uma classe filha
            # (AtividadeForm ou MaterialForm), ele automaticamente cria
            # a instância da classe pai (ItemAcademico) e a filha,
            # preenchendo o campo 'tipo' e 'arquivo' na classe pai.
            item = form.save(commit=False) # Salva a instância, mas não a persiste ainda
            item.tipo = tipo # Atribui o tipo antes de salvar
            item.save() # Salva a instância no banco de dados
            # Se você tem relacionamentos ManyToMany ou lógica pós-save, faria aqui
            # Por exemplo, form.save_m2m() se tivesse campos ManyToMany

            return redirect('itemacademico:index')
    else: # GET request
        if tipo == 'ATIVIDADE':
            form = AtividadeForm(initial={'tipo': 'ATIVIDADE'}) # Pré-preenche o campo 'tipo'
        elif tipo == 'MATERIAL':
            form = MaterialForm(initial={'tipo': 'MATERIAL'}) # Pré-preenche o campo 'tipo'
        else:
            form = ItemAcademicoForm() # Fallback

    return render(request, 'itemacademico/cria.html', {
        'form': form,
        'tipo_selecionado': tipo
    })

# Atualização de atividade ou material
def atualiza(request, id_itemacademico):
    # Obtém a instância do ItemAcademico pai
    item_academico_pai = get_object_or_404(ItemAcademico, pk=id_itemacademico)

    # Verifica se é uma Atividade ou Material para carregar a instância correta
    # e o formulário correto
    instance = None
    FormClass = None

    try:
        instance = item_academico_pai.atividade # Tenta obter a instância de Atividade
        FormClass = AtividadeForm
    except Atividade.DoesNotExist:
        try:
            instance = item_academico_pai.material # Tenta obter a instância de Material
            FormClass = MaterialForm
        except Material.DoesNotExist:
            # Se não for nem Atividade nem Material, pode ser um ItemAcademico "genérico"
            # ou um erro na lógica. Para este caso, vamos assumir que sempre será um dos dois.
            # Caso contrário, você pode usar ItemAcademicoForm aqui.
            instance = item_academico_pai
            FormClass = ItemAcademicoForm # Fallback se necessário, mas ajuste o template

    if request.method == 'POST':
        # Correção: Use a variável 'instance' corretamente
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('itemacademico:index')
    else:
        # Correção: Use a variável 'instance' corretamente para inicializar o formulário
        form = FormClass(instance=instance)

    # Correção: 'itemacademico' não está definido no contexto do template aqui
    return render(request, 'itemacademico/atualiza.html', {'form': form, 'item': instance})


# Exclusão de atividade ou material
def deleta(request, id_itemacademico):
    item = get_object_or_404(ItemAcademico, id=id_itemacademico)

    if request.method == 'POST':
        item.delete() # Ao deletar o ItemAcademico pai, o Django deleta as subclasses
        return redirect('itemacademico:index')

    # Correção: 'itemacademico' não está definido no contexto do template aqui
    return render(request, 'itemacademico/deleta.html', {'item': item})