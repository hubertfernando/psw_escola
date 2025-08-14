from django.urls import path
from . import views

app_name = 'turma'

urlpatterns = [
    path('', views.index, name='index-turma'),
    path('<int:id_turma>/', views.detalhe, name='detalhe-turma'),
    path('add/', views.cria, name='add-turma'),
    path('edit/<int:id_turma>/', views.atualiza, name='edit-turma'),
    path('delete/<int:id_turma>/', views.deleta, name='delete-turma'),
    path('entrar/', views.entrar_por_codigo, name='entrar_turma'), 
    path('<int:id_turma>/disciplinas/', views.disciplinas_da_turma, name='disciplinas-da-turma'),

]
