from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

from disciplina import views as views_disciplina
from aluno import views as views_aluno
from turma import views as views_turma

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conta/', include('django.contrib.auth.urls')),
    path('disciplina/', include(('disciplina.urls', 'disciplina'), namespace='disciplina')),
    path('aluno/', include('aluno.urls')),
    path('itemacademico/', include('itemacademico.urls')),
    path('turma/', include('turma.urls')),
    path('comentario/', include(('comentario.urls', 'comentario'), namespace='comentario')),
]

# arquivos de mídia (imagens enviadas pelos alunos, por exemplo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)