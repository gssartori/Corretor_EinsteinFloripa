from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import NovoStorage
from relatorios.functions import utils
from relatorios.functions.corretor_simulinho import cria_simulados


def index(request):
    dados = dict()

    if request.method == 'POST':
        arquivos_recebidos = request.FILES.getlist('dados_simulinho')

        if utils.valida_nome_uploads(sorted([arquivo.name for arquivo in arquivos_recebidos])):
            for arquivo in arquivos_recebidos:
                NovoStorage().save(arquivo.name, arquivo)
            utils.memo.clear()
            utils.cria_json()

        return HttpResponseRedirect(reverse('index'))

    alertas = utils.le_arquivo('alertas')
    if alertas: dados['alertas'] = alertas

    dados['relatorios'] = utils.le_arquivo('relatorios')

    return render(request, 'index.html', dados)


def atualiza_pagina_ajax(request):
    return JsonResponse(utils.verifica_dados())


def envia_relatorios(request):
    if request.GET.get('btn_envia_email'):
        cria_simulados(nome_aluno=request.GET.get('envia_email'), enviar_email=True)

    elif request.GET.get('btn_envia_emails'):
        cria_simulados(enviar_email=True)

    return HttpResponseRedirect(reverse('index'))


def limpa_media(request):
    utils.limpa_dados()
    return HttpResponseRedirect(reverse('index'))


def exporta_pdf(request):
    if (request.GET.get('btn_download_pdf')):
        nome_aluno = request.GET.get('download_pdf')
        pdf = cria_simulados(nome_aluno, enviar_email=False)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            nome_arquivo = "%s.pdf" %(nome_aluno)
            content = "inline; filename='%s'" % (nome_arquivo)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (nome_arquivo)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("PDF não encontrado")

