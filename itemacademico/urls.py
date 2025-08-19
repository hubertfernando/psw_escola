from django.urls import path
from . import views

app_name = 'itemacademico'

urlpatterns = [
    path('', views.index, name='index'),
    path('disciplina/<int:disciplina_id>/', views.itens_por_disciplina, name='itens_por_disciplina'),
    path('disciplina/<int:disciplina_id>/add/', views.cria, name='cria'),  
    path('edit/<int:id_itemacademico>/', views.atualiza, name='atualiza'),
    path('delete/<int:id_itemacademico>/', views.deleta, name='deleta'),
    path('<int:id_itemacademico>/', views.detalhe, name='detalhe'),
]
