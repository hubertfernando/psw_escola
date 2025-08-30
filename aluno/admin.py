# aluno/admin.py
from django.contrib import admin
from .models import Aluno  # modelo do app aluno

# -------------------------
# Admin para Aluno
# -------------------------
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'username', 'matricula', 'telefone', 'ingresso_sistema')
    search_fields = ('nome', 'username', 'matricula')
    readonly_fields = ('ingresso_sistema',)

    # Somente superuser pode deletar alunos
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


