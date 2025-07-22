from django.db import models

# Model de disciplina
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    

    def __str__(self):
        return self.nome