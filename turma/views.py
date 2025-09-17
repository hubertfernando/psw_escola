from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from urllib.parse import urlparse, parse_qs
from .models import Turma
from .forms import TurmaForm
from disciplina.models import Disciplina 


@login_required
def index(request):
    turmas = Turma.objects.filter(membros=request.user)
    return render(request, 'turma/index.html', {
        'turmas': turmas,
        'request': request,  # necessário para template
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
        'request': request,
    })


@login_required
def cria(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            turma.lider = request.user
            turma.save()
            turma.membros.add(request.user)

            # 🔹 Adiciona permissões oficiais do Django ao líder
            perm_change = Permission.objects.get(codename='change_turma')
            perm_delete = Permission.objects.get(codename='delete_turma')
            request.user.user_permissions.add(perm_change, perm_delete)
            request.user.refresh_from_db()  # garante que as permissões sejam reconhecidas imediatamente

            return redirect("/turma/")
    else:
        form = TurmaForm()
    return render(request, 'turma/cria.html', {'form': form})


@login_required
@permission_required('turma.change_turma', raise_exception=True)
def atualiza(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)
    form = TurmaForm(request.POST or None, instance=turma)
    if form.is_valid():
        form.save()
        return redirect("/turma/")
    return render(request, 'turma/atualiza.html', {'form': form})


@login_required
@permission_required('turma.delete_turma', raise_exception=True)
def deleta(request, id_turma):
    turma = get_object_or_404(Turma, pk=id_turma)
    turma.delete()
    return redirect('/turma/')


@login_required
def entrar_por_codigo(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo_convite', '').strip()

        # Extrai código do link completo, se necessário
        if codigo.startswith('http'):
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
        'disciplinas': disciplinas,
        'request': request,
    })
