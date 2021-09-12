from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('exporta-pdf', views.exporta_pdf, name='exporta-pdf')
    # Para abrir em nova guia 1 link para cada relatório guardado no server, verificar se criar esse path é necessário
    # path('exemplo_relatorios', views.relatorio, 'relatorio')
]