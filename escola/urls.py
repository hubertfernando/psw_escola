from django.contrib import admin
from django.urls import path, include 

from disciplina import views as views_disciplina
from aluno import views as views_aluno

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conta/', include('django.contrib.auth.urls')),
    path('disciplina/', include('disciplina.urls')),
    path('aluno/', include('aluno.urls')),
]
