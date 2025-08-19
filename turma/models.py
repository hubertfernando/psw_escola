import string
import random
from django.db import models
from django.contrib.auth.models import User

def gerar_codigo_aleatorio(tamanho=8):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

class Turma(models.Model):
    ANO_CHOICES = [
        ('1° Ano', '1° Ano'),
        ('2° Ano', '2° Ano'),
        ('3° Ano', '3° Ano'),
    ]

    CURSO_CHOICES = [
        ('AA', 'AA'),
        ('AB', 'AB'),
        ('BA', 'BA'),
        ('BII', 'BII'),
        ('AII', 'AII'),
    ]

    curso = models.CharField(max_length=4, choices=CURSO_CHOICES)
    ano = models.CharField(max_length=10, choices=ANO_CHOICES)
    data_criacao = models.DateTimeField(auto_now_add=True)

    lider = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lider_turmas'
    )
    membros = models.ManyToManyField(
        User,
        blank=True,
        related_name='turmas'
    )

    codigo_convite = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "Turma"

    def __str__(self):
        return f"{self.get_ano_display()} - {self.get_curso_display()}"

    def get_link_convite(self):
        if self.codigo_convite:
            return f"/turma/entrar/?codigo={self.codigo_convite}"
        return ""

    def save(self, *args, **kwargs):
        if not self.codigo_convite:
            novo_codigo = gerar_codigo_aleatorio()
            while Turma.objects.filter(codigo_convite=novo_codigo).exists():
                novo_codigo = gerar_codigo_aleatorio()
            self.codigo_convite = novo_codigo
        super().save(*args, **kwargs)
