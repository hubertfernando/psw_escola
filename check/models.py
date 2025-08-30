from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User  # Adicione esta importação

class Checklist(models.Model):
    PRIORIDADE_ALTA = 'alta'
    PRIORIDADE_MEDIA = 'media' 
    PRIORIDADE_BAIXA = 'baixa'
    
    PRIORIDADE_CHOICES = [
        (PRIORIDADE_ALTA, 'Alta'),
        (PRIORIDADE_MEDIA, 'Média'),
        (PRIORIDADE_BAIXA, 'Baixa'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    disciplina = models.ForeignKey(
        'disciplina.Disciplina',
        on_delete=models.CASCADE,
        verbose_name="Disciplina"
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_entrega = models.DateField(verbose_name="Data de Entrega")
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default=PRIORIDADE_MEDIA,
        verbose_name="Prioridade"
    )
    concluido = models.BooleanField(default=False, verbose_name="Concluído")
    
    # ADICIONE ESTE CAMPO - é crucial para o controle de permissões
    usuario = models.ForeignKey(
        User,  # Modelo de usuário do Django
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name='checklists'
    )
    
    class Meta:
        verbose_name = "Checklist"
        verbose_name_plural = "Checklists"
        ordering = ['data_entrega', 'prioridade']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('checklist_detalhe', kwargs={'pk': self.pk})
    
    def alternar_status(self):
        self.concluido = not self.concluido
        self.save()
    
    def dias_para_entrega(self):
        hoje = timezone.now().date()
        return (self.data_entrega - hoje).days
    
    def esta_atrasado(self):
        return self.dias_para_entrega() < 0 and not self.concluido