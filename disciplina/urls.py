from django.urls import path
from . import views # Importa as views do próprio app

# Urls de disciplina
urlpatterns = [
    path('', views.index, name='index-disciplina'),
    path('<int:id_disciplina>/', views.detalha, name='index-detalha'),
    path('cria/', views.cria, name='cria-disciplina'),
    path('atualiza/<int:id_disciplina>', views.atualiza, name='atualiza-disciplina'),
    path('delete/<int:id_disciplina>', views.delete, name='delete-disciplina')
]