from django.db import models


class Atividade(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateTimeField()
    arquivo = models.FileField(upload_to='atividades/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.titulo}"

