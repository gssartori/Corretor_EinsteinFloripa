from django.shortcuts import render
from .models import Relatorio, NovoStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage, default_storage
import pandas as pd
import json

# Create your views here.

def index(request):
    # relatorios = Relatorio.objects.all()
    dados = dict()# {'relatorios': relatorios}

    def trata_arquivo(arquivo):
        """
        Função verifica o tipo do :arquivo: recebido e retorna os dados
        no formato .json, por ser mais leve e fácil de utilizar
        """
        tipo_arquivo = arquivo.name.split(".")[-1]

        if tipo_arquivo in ('xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'): arquivo = pd.read_excel(arquivo)
        elif tipo_arquivo == 'json': arquivo = pd.read_json(arquivo)
        elif tipo_arquivo == 'csv': arquivo = pd.read_csv(arquivo)
        else: return None
        return arquivo.sort_values(by=['Nome'], ascending=True).to_json(orient='records', force_ascii=False)

    if request.method == 'POST':
        # Primeiro: descobrir como colocar um alert sempre que um novo request.files for acionado, perguntar
        # pro user se ele quer mesmo trocar, e perder seus dados.....
        arquivo_recebido = trata_arquivo(request.FILES['planilha'])

        with default_storage.open('dados.json', mode='w') as arquivo_json:
            json.dump(json.loads(arquivo_recebido), arquivo_json, ensure_ascii=False)
            print('ARQUIVO RECEBIDO: ',arquivo_recebido)
        return HttpResponseRedirect(reverse('index'))

        # arquivo_armazenado = NovoStorage()
        # nome_arquivo = arquivo_armazenado.save('dados.json', arquivo_recebido)
        # arquivo_json = trata_arquivo(nome_arquivo)
        # dados['url'] = arquivo_armazenado.url(nome_arquivo)
        # print("ERROR!!! Coloque um arquivo com tipo válido: \n 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'csv'")
        # dados['type_error'] = "Insira um arquivo com tipo válido: \n 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'csv'"

    with default_storage.open('dados.json', mode='r') as arquivo:
        dados['relatorios'] = json.loads(arquivo.read())

    # status_relatorio = pd.read_json('dados.json')
    # if not status_relatorio.empty:
    #     dados['relatorio'] = status_relatorio
    return render(request, 'index.html', dados)