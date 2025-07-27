from django.db import models

class Checklist (models.Model):
    # Campo de texto para o nome da tarefa
    titulo = models.CharField(max_length=200)
    
    # Campo de texto para a disciplina relacionada à tarefa
    disciplina = models.CharField(max_length=100)
    
    # Campo de data para a data de entrega da tarefa
    data_entrega = models.DateField()
    
    # Campo booleano para saber se a tarefa foi concluída ou não
    concluido = models.BooleanField(default=False)
    
    # Campo numérico para definir a prioridade da tarefa (1 a 5)
    prioridade = models.IntegerField()

    def __str__(self):
        return self.titulo

