from django.db import models

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
    lider = models.CharField(max_length=255, default='Sem líder')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Turma"

    def __str__(self):
        return f"{self.get_ano_display()} - {self.get_curso_display()}"
