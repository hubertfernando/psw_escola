from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from turma import views as turma_views
from atividade import views as atividade_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas turma
    path('turma/', turma_views.index, name='index-turma'),
    path('turma/<int:id_turma>/', turma_views.detalhe, name='detalhe-turma'),
    path('turma/add/', turma_views.cria, name='cria-turma'),
    path('turma/update/<int:id_turma>/', turma_views.atualiza, name='atualiza-turma'),
    path('turma/delete/<int:id_turma>/', turma_views.deleta, name='delete-turma'),

    # Rotas atividade
    path('atividade/', atividade_views.index, name='index-atividade'),
    path('atividade/<int:id_atividade>/', atividade_views.detalhe, name='detalhe-atividade'),
    path('atividade/add/', atividade_views.cria, name='cria-atividade'),
    path('atividade/update/<int:id_atividade>/', atividade_views.atualiza, name='atualiza-atividade'),
    path('atividade/delete/<int:id_atividade>/', atividade_views.deleta, name='delete-atividade'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
