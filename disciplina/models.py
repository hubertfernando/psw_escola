from django.db import models
from turma.models import Turma

# Model de disciplina
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome
