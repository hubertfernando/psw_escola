from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Turma
from .forms import TurmaForm
from disciplina.models import Disciplina 

@login_required
def index(request):
    turmas = Turma.objects.filter(membros=request.user)
    # verifica se o usuário está no grupo Líder
    is_lider = request.user.groups.filter(name="Líder").exists()
    return render(request, 'turma/index.html', {
        'turmas': turmas,
        'is_lider': is_lider
    })


@login_required
def detalhe(request, id_turma):
    turma = get_object_or_404(Turma, id=id_turma)
    link_convite_completo = request.build_absolute_uri(turma.get_link_convite())
    alunos = turma.membros.all()
    return render(request, 'turma/detalhe.html', {
        'turma': turma,
        'link_convite_completo': link_convite_completo,
        'alunos': alunos,
    })


@login_required
def cria(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            turma.lider = request.user
            turma.save()
            turma.membros.add(request.user)  # adiciona o criador como membro

            # adiciona usuário ao grupo Líder
            lider_group, _ = Group.objects.get_or_create(name="Líder")
            request.user.groups.add(lider_group)
            request.user.save()

            return HttpResponseRedirect("/turma/")
    else:
        form = TurmaForm()
    return render(request, 'turma/cria.html', {'form': form})


@login_required
def atualiza(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)

    # só o líder da turma pode editar
    if turma.lider != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar esta turma.")

    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/turma/")
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'turma/atualiza.html', {'form': form})


@login_required
def deleta(request, id_turma):
    turma = get_object_or_404(Turma, id=id_turma)

    # só o líder da turma pode excluir
    if turma.lider != request.user:
        return HttpResponseForbidden("Você não tem permissão para excluir esta turma.")

    turma.delete()
    return HttpResponseRedirect('/turma/')


@login_required
def entrar_por_codigo(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo_convite', '').strip()

        # Extrai código do link completo, se for o caso
        if codigo.startswith('http'):
            from urllib.parse import urlparse, parse_qs
            url_parts = urlparse(codigo)
            query_params = parse_qs(url_parts.query)
            codigo_lista = query_params.get('codigo')
            if codigo_lista:
                codigo = codigo_lista[0]
            else:
                return redirect('turma:index-turma')

        turma = get_object_or_404(Turma, codigo_convite=codigo)
        if request.user not in turma.membros.all():
            turma.membros.add(request.user)

        return redirect('turma:index-turma')

    return redirect('turma:index-turma')


@login_required
def disciplinas_da_turma(request, id_turma):
    turma = get_object_or_404(Turma, id=id_turma)
    disciplinas = Disciplina.objects.filter(turma=turma)
    return render(request, 'disciplina/index.html', {
        'turma': turma,
        'disciplinas': disciplinas
    })
