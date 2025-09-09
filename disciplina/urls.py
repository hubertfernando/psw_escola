from django.urls import path
from . import views

app_name = 'disciplina'  

urlpatterns = [
    path('', views.index, name='index-disciplina'),
    path('<int:id_disciplina>/', views.detalha, name='index-detalha'),
     path('cria/<int:turma_id>/', views.cria, name='cria_disciplina'),  
    path('atualiza/<int:id_disciplina>/', views.atualiza, name='atualiza-disciplina'),
    path('delete/<int:id_disciplina>/', views.delete, name='delete-disciplina'),
]
