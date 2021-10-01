from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('envia_relatorios', views.envia_relatorios, name='envia_relatorios'),
    path('status_relatorios_ajax', views.status_relatorios_ajax, name='status_relatorios_ajax')
    # path('exporta-pdf', views.exporta_pdf, name='exporta-pdf')
    # Para abrir em nova guia 1 link para cada relatório guardado no server, verificar se criar esse path é necessário
    # path('exemplo_relatorios', views.relatorio, 'relatorio')
]