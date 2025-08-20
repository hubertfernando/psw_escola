from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Checklist(models.Model):
    # Básico
    titulo = models.CharField(max_length=200)
    disciplina = models.CharField(max_length=100)
    data_entrega = models.DateField()

    # Status
    concluido = models.BooleanField(default=False)

    # Prioridade (1 a 5)
    prioridade = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # Metadados úteis para checklist
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Padrão: pendentes primeiro, depois concluídos; maior prioridade antes; data mais próxima antes
        ordering = ('concluido', '-prioridade', 'data_entrega', 'pk')

    def __str__(self):
        return self.titulo

    # Métodos de domínio para ficar igual à experiência do Google (marcar/alternar rápido)
    def marcar_concluido(self):
        self.concluido = True
        if not self.completed_at:
            self.completed_at = timezone.now()
        self.save(update_fields=['concluido', 'completed_at', 'updated_at'])

    def marcar_pendente(self):
        self.concluido = False
        self.completed_at = None
        self.save(update_fields=['concluido', 'completed_at', 'updated_at'])

    def alternar_status(self):
        if self.concluido:
            self.marcar_pendente()
        else:
            self.marcar_concluido()

