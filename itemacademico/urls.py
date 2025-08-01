from django.urls import path
from . import views

app_name = 'itemacademico'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id_itemacademico>/', views.detalhe, name='detalhe'),
    path('add/', views.cria, name='add'),
    path('edit/<int:id_itemacademico>/', views.atualiza, name='edit'),
    path('delete/<int:id_itemacademico>/', views.deleta, name='delete'),
]
