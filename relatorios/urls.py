from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^envia_relatorios$', views.envia_relatorios, name='envia_relatorios'),
    url(r'^atualiza_pagina_ajax$', views.atualiza_pagina_ajax, name='atualiza_pagina_ajax'),
    url(r'^exporta_pdf$', views.exporta_pdf, name='exporta_pdf'),
    url(r'^limpa_media$', views.limpa_media, name='limpa_media')
]
