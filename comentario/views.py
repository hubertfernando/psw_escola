from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comentario
from .forms import ComentarioForm
from itemacademico.models import ItemAcademico

@login_required
def index(request, id_item):
    item = get_object_or_404(ItemAcademico, pk=id_item)
    comentarios = Comentario.objects.filter(item=item, parent__isnull=True).order_by('-criado_em')
    return render(request, 'comentario/index.html', {'item': item, 'comentarios': comentarios})


@login_required
def detalhe(request, id_comentario):
    comentario = get_object_or_404(Comentario, pk=id_comentario)
    respostas = comentario.respostas.all().order_by('-criado_em')
    return render(request, 'comentario/detalhe.html', {
        'comentario': comentario,
        'respostas': respostas
    })

@login_required
def cria(request, id_item):
    item = get_object_or_404(ItemAcademico, pk=id_item)
    parent_id = request.GET.get('parent')
    parent_comentario = None
    if parent_id:
        parent_comentario = get_object_or_404(Comentario, pk=parent_id, item=item)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.item = item
            comentario.autor = request.user
            comentario.parent = parent_comentario
            comentario.save()
            return redirect('comentario:index', id_item=item.id)
    else:
        form = ComentarioForm()

    return render(request, 'comentario/cria.html', {
        'form': form,
        'item': item,
        'parent': parent_comentario
    })

@login_required
def atualiza(request, id_comentario):
    comentario = get_object_or_404(Comentario, pk=id_comentario, autor=request.user)
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('comentario:index', id_item=comentario.item.id)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'comentario/atualiza.html', {'form': form, 'comentario': comentario})

@login_required
def deleta(request, id_comentario):
    comentario = get_object_or_404(Comentario, pk=id_comentario, autor=request.user)
    item_id = comentario.item.id
    comentario.delete()
    return redirect('comentario:index', id_item=item_id) 
