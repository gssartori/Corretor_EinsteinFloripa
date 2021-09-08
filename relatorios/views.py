from django.shortcuts import render
from .models import Relatorio, NovoStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from relatorios.functions import utils

def index(request):
    # relatorios = Relatorio.objects.all()
    dados = dict()# {'relatorios': relatorios}
    utils.alertas.clear()

    if request.method == 'POST':
        arquivo_recebido = utils.converte_arquivo(request.FILES['planilha']) \
            if 'planilha' in request.FILES else False

        if arquivo_recebido:
            utils.escreve_arquivo(arquivo_recebido)

        return HttpResponseRedirect(reverse('index'))

        # arquivo_armazenado = NovoStorage()
        # nome_arquivo = arquivo_armazenado.save('dados.json', arquivo_recebido)
        # arquivo_json = trata_arquivo(nome_arquivo)
        # dados['url'] = arquivo_armazenado.url(nome_arquivo)
        # print("ERROR!!! Coloque um arquivo com tipo válido: \n 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'csv'")
        # dados['type_error'] = "Insira um arquivo com tipo válido: \n 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'csv'"
    dados['relatorios'] = utils.le_arquivo()[0]['relatorios']
    if utils.alertas:
        dados['alertas'] = utils.alertas

    # status_relatorio = pd.read_json('dados.json')
    # if not status_relatorio.empty:
    #     dados['relatorio'] = status_relatorio
    return render(request, 'index.html', dados)