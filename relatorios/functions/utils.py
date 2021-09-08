from django.core.files.storage import default_storage

import pandas as pd
import json

alertas = []    # lista de dicionários

def dispara_alerta(titulo, mensagem):
    """
    Método armazena o conteúdo do alerta na variável global 'alertas', que
    será lido no próximo reload da página principal 'index.html' da views.py
    """
    pass
    # alertas.append({'titulo':titulo, 'mensagem':mensagem})


def converte_arquivo(arquivo):
    """
    Função verifica o tipo do :arquivo: recebido e converte os dados
    no formato .json
    """
    tipo_arquivo = arquivo.name.split(".")[-1]

    if tipo_arquivo in ('xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'): arquivo = pd.read_excel(arquivo)
    elif tipo_arquivo == 'json': arquivo = pd.read_json(arquivo)
    elif tipo_arquivo == 'csv': arquivo = pd.read_csv(arquivo)
    else: return None

    return arquivo.sort_values(by=['Nome'], ascending=True).to_json(orient='records', force_ascii=False)


def escreve_arquivo(relatorios = None):
    """
    Função responsável por escrever algo no arquivo dados.json

    Obs: o arquivo dados.json deve ser dividido em 2 partes principais:
        1. relatorios: armazena lista com dicionários dos dados dos relatórios
           (aluno, status_de_envio, email, data...)
        2. alertas: armazena lista com dicionário dos alertas, advertências, mensagens de sucesso...
           (titulo, mensagem)
    """
    try:
        with default_storage.open('dados.json', mode='w') as arquivo_json:
            if relatorios:
                dados = [{"relatorios": json.loads(relatorios)}]            # "alertas": alertas
                json.dump(dados, arquivo_json, ensure_ascii=False)

            else:
                dados = [{"relatorios": le_arquivo()[0]['relatorios']}]     # "alertas": alertas
                json.dump(json.loads(dados), arquivo_json, ensure_ascii=False)

    except Exception as e:
        # escreve_arquivo('[]')
        alertas.append({"titulo": "Arquivo Corrompido", "mensagem":e}) # dispara_alerta("Arquivo Corrompido", e)

def le_arquivo():
    try:
        alertas.append({"titulo": "Alerta de Teste", "mensagem": "TUDO ERRADO IRMÃO"})
        with default_storage.open('dados.json', mode='r') as arquivo_json:
            return json.loads(arquivo_json.read())
    except Exception as e:
        if str(e) == 'Expecting value: line 1 column 1 (char 0)':
            # escreve_arquivo('[]')
            alertas.append({"titulo": "Alerta de Teste", "mensagem": e})  # dispara_alerta("Arquivo Corrompido", e)
            return json.loads('[{"relatorios": [], "alertas": []}]')



