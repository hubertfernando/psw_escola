from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from .models import Aluno
from .forms import AlunoCreationForm, UsuarioEditForm, AlunoEditForm

@login_required
@permission_required('aluno.view_aluno', raise_exception=True)
def index(request):
    alunos = Aluno.objects.all()
    return render(request, 'aluno/index.html', {'alunos': alunos})

@login_required
@permission_required('aluno.detail_aluno', raise_exception=True)
def detalha(request, id_aluno):
    aluno = get_object_or_404(Aluno, id=id_aluno)
    return render(request, 'aluno/detalha.html', {'aluno': aluno})

@login_required
@permission_required('aluno.add_aluno', raise_exception=True)
def cria(request):
    if request.method == 'POST':
        form = AlunoCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/aluno/")
    else:
        form = AlunoCreationForm()
    return render(request, 'aluno/cria.html', {'form': form})

@login_required
@permission_required('aluno.change_aluno', raise_exception=True)
def atualiza(request, id_aluno):
    aluno = get_object_or_404(Aluno, id=id_aluno)
    user = aluno.user

    if request.method == 'POST':
        usuario_form = UsuarioEditForm(request.POST, instance=user)
        aluno_form = AlunoEditForm(request.POST, instance=aluno)

        if usuario_form.is_valid() and aluno_form.is_valid():
            usuario_form.save()
            aluno_form.save()
            messages.success(request, "Aluno atualizado com sucesso!")
            return redirect('index')
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        usuario_form = UsuarioEditForm(instance=user)
        aluno_form = AlunoEditForm(instance=aluno)

    return render(request, 'aluno/atualiza.html', {
        'usuario_form': usuario_form,
        'aluno_form': aluno_form,
    })

@login_required
@permission_required('aluno.delete_aluno', raise_exception=True)
def delete(request, id_aluno):
    aluno = get_object_or_404(Aluno, id=id_aluno)
    aluno.user.delete()  # Apaga também o usuário vinculado
    aluno.delete()
    return HttpResponseRedirect("/aluno/")