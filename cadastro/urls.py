from django.urls import path
from . import views

app_name='cadastro'

urlpatterns = [
    path('unidade', views.unidade_list, name='unidade_list'),
    path('unidade/cadastrar', views.unidade_create, name='unidade_create'),
]