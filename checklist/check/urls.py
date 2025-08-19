from django.urls import path
from . import views

urlpatterns = [
    path('', views.checklist_base, name='checklist_list'),
    path('editar/<int:pk>/', views.checklist_base, name='checklist_edit_inline'),
    path('deletar/<int:pk>/', views.checklist_delete_inline, name='checklist_delete_inline'),
    path('cancelar/', views.checklist_clear_form, name='checklist_clear_form'),
    path('toggle/<int:pk>/', views.checklist_toggle, name='checklist_toggle'),

]
