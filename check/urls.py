from django.urls import path
from . import views

urlpatterns = [
    path('', views.checklist_lista, name='checklist_lista'),
    path('novo/', views.checklist_criar, name='checklist_criar'),
    path('editar/<int:pk>/', views.checklist_editar, name='checklist_editar'),
    path('detalhe/<int:pk>/', views.checklist_detalhe, name='checklist_detalhe'),
    path('deletar/<int:pk>/', views.checklist_deletar, name='checklist_deletar'),
    path('cancelar/', views.checklist_cancelar, name='checklist_cancelar'),
    path('alternar/<int:pk>/', views.checklist_alternar, name='checklist_alternar'),
    path('calendario/', views.checklist_calendario, name='checklist_calendario'),
    path('atualiza-data/<int:pk>/', views.checklist_atualiza_data, name='checklist_atualiza_data'),
]
