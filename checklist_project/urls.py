from django.contrib import admin
from django.urls import path, include  # 👈 import necessário

urlpatterns = [
    path('admin/', admin.site.urls),
    path('check/', include('check.urls')),  # 👈 adiciona as rotas do app "check"
]
