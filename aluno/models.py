from django.db import models
from django.contrib.auth.models import User

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno')
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    # turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True)
    # foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
    ingresso_sistema = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alunos_alunos"
        permissions = [
            ("detail_aluno", "Detalha o aluno"),
        ]

    def __str__(self):
        return self.nome