"""
    Este arquivo serve para colocar a função que vocês colocariam no Jupyter.
    Assim, todos os arquivos .pickle utilizados não precisarão serem salvos no
    computador do usuário
"""

import pandas as pd
from relatorios.functions.utils import alertas

def trata_arquivo(arquivos_recebidos):
    """
    Método manipula os dados de cada um dos arquivos enviados pelo 'input',
    e verifica se existem erros nos arquivos

    Arquivos permitidos:
    'redacao' => (redação de cada aluno)
    'dados_pessoais' => (nome e cpf de cada aluno)
    'gabarito_oficial' => (gabarito oficial para turma A)
    'respostas_alunos_b' => (respostas dos alunos)

    :return:
    Retorna True se o programa está pronto para gerar os .PDFs
    Retorna False caso contrário
    """
    dados_pessoais, gabarito, data, redacao = None, None, None, None

    for arquivo in arquivos_recebidos:
        nome_tipo = arquivo.name.split(".")

        if nome_tipo[-1] in ('xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'):

            if nome_tipo[0] == 'dados_pessoais':
                dados_pessoais = pd.read_excel(arquivo)
            elif nome_tipo[0] == 'gabarito_oficial':
                gabarito = pd.read_excel(arquivo)
            elif nome_tipo[0] == 'respostas_alunos_b':
                data = pd.read_excel(arquivo)
            elif nome_tipo[0] == 'redacao':
                redacao = pd.read_excel(arquivo)
            else:
                alertas.append({"titulo": f"Nome '{arquivo[0]}' de arquivo inválido",
                                      "mensagem": "ERROR!!! Coloque um arquivo com nome válido: \n "
                                                  "'dados_pessoais', 'gabarito_oficial', 'redacao', 'respostas_alunos_b'"})
                return False
        else:
            alertas.append({"titulo": f"Tipo '{arquivo[0]}' de arquivo inválido",
                            "mensagem": "ERROR!!! Coloque um arquivo com tipo válido: \n "
                                        "'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'csv'"})
            return False

    cria_pickles(dados_pessoais, gabarito, data, redacao)






