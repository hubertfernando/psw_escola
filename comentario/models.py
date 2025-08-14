from django.db import models
# Create your models here.
from itemacademico.models import ItemAcademico  
from django.contrib.auth.models import User  

class Comentario(models.Model):
    texto = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemAcademico, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='respostas', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comentário de {self.autor} no item {self.item}'
