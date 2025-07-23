from django.urls import path
from . import views # Importa as views do próprio app

# Urls de aluno
urlpatterns = [
    path('', views.index, name='index-aluno'),
    path('<int:id_aluno>/', views.detalha, name='index-detalha'),
    path('cria/', views.cria, name='cria-aluno'),
    path('atualiza/<int:id_aluno>', views.atualiza, name='atualiza-aluno'),
    path('delete/<int:id_aluno>/', views.delete, name='delete-aluno')
]