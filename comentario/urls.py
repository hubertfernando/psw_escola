from django.urls import path
from . import views

app_name = 'comentario'

urlpatterns = [
    path('<int:id_item>/', views.index, name='index'),  # lista comentários de um item
    path('detalhe/<int:id_comentario>/', views.detalhe, name='detalhe'),  # detalhe do comentário
    path('cria/<int:id_item>/', views.cria, name='cria'),  # cria comentário (ou resposta) para item
    path('atualiza/<int:id_comentario>/', views.atualiza, name='atualiza'),
    path('deleta/<int:id_comentario>/', views.deleta, name='deleta'),
]
