from django.db import models

TIPOS = [
    ('ATIVIDADE', 'Atividade'),
    ('MATERIAL', 'Material de Apoio'),
]

class ItemAcademico(models.Model):
    tipo = models.CharField(max_length=10, choices=TIPOS)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='itens_academicos/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"

class Atividade(ItemAcademico):
    data_entrega = models.DateTimeField()

class Material(ItemAcademico):
    pass
