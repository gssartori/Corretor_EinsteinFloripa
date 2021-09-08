from django.core.files.storage import default_storage
import pandas as pd
import json, datetime

alertas = []    # lista de dicionários
memo = {}       # memorizador do dados.json {'nome_aluno': index}

def proximo_status(status_atual, erro = False):
    """
      Função retorna o próximo status do aluno, de acordo com seu status atual,
      seguindo a seguinte ordem:
        *None --> Pendente --> Gerando --> Enviando --> Enviado || Não Enviado (se erro=True)

      Obs: Caso não esteja em algum desses 3 estados, ocorreu algum erro
    """
    if not status_atual:
        return 'Pendente'
    elif (status_atual == 'Pendente'):
        return 'Gerando'
    elif (status_atual == 'Gerando'):
        return 'Enviando'
    elif (any(status_atual == 'Enviando', status_atual == 'Não Enviado')):
        return 'Enviado' if not erro else 'Não Enviado'
    else:
        alertas.append({"titulo": "Error", "mensagem": "Status não reconhecido proximo_status()"})
        return 'None'


def edita_status(nome_aluno, erro=False):
    """
      Método responsável por buscar e alterar o estado do relatório do aluno pelo seu nome;
      A busca realizada é do tipo binária, e é delimitada aos alunos cujos estados são
      diferentes de 'Enviado' / 'Enviando'

      Obs: o arquivo.json é ordenado pelo 'Status' e 'Nome' do aluno, respectivamente.
    """
    dados_aluno = le_arquivo()[0]['relatorios']

    inicio = 0
    fim = len(dados_aluno) - 1
    encontrou = False

    if nome_aluno in memo:
        index = memo[nome_aluno]
        dados_aluno[index]['Status'] = proximo_status(dados_aluno[index]["Status"])

    else:
        # Busca binária
        while (inicio <= fim and not encontrou):
            meio = (inicio + fim) // 2
            if dados_aluno[meio]['Nome'].lower() == nome_aluno.lower():
                dados_aluno[meio]['Status'] = proximo_status(dados_aluno[meio]["Status"])
                memo[nome_aluno] = meio
                encontrou = True
            else:
                if nome_aluno.lower() < dados_aluno['Nome'][meio].lower():
                    fim = meio - 1
                else:
                    inicio = meio + 1

        if not encontrou:
            # Busca linear, caso a busca binária não encontre
            for i, aluno in enumerate(dados_aluno):
                if (aluno['Nome'].lower() == nome_aluno.lower()):
                    aluno["Status"] = proximo_status(aluno["Status"])
                    print('!!!!Busca Linear@@@@@')
                    encontrou = True
                    memo[nome_aluno] = i
                    break

    if not encontrou:
        aluno["Status"] = "ERROR <-- Aluno não encontrado no JSON -->"
    else:
        dados_editados = json.dumps([{'relatorios': dados_aluno}])
        escreve_arquivo(dados_editados)


def converte_arquivo(arquivo):
    """
    Função verifica o tipo do :arquivo: recebido e converte os dados
    no formato .json
    """
    tipo_arquivo = arquivo.name.split(".")[-1]

    if tipo_arquivo in ('xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'): arquivo = pd.read_excel(arquivo)
    elif tipo_arquivo == 'json': arquivo = pd.read_json(arquivo)
    elif tipo_arquivo == 'csv': arquivo = pd.read_csv(arquivo)
    else:
        alertas.append({"titulo": "Tipo de arquivo inválido",
                        "mensagem": "ERROR!!! Coloque um arquivo com tipo válido: \n "
                                    "'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'json', 'csv'"})
        return None

    return arquivo.sort_values(by=['Nome'], ascending=True).to_json(orient='records', force_ascii=False)


def escreve_arquivo(relatorios):
    """ Função responsável por escrever algo no arquivo dados.json """
    try:
        with default_storage.open('dados.json', mode='w') as arquivo_json:
            json.dump([{"relatorios": json.loads(relatorios)}], arquivo_json, ensure_ascii=False)

    except Exception as e:
        alertas.append({"titulo": "Arquivo Corrompido", "mensagem":e}) # dispara_alerta("Arquivo Corrompido", e)

def le_arquivo():
    try:
        with default_storage.open('dados.json', mode='r') as arquivo_json:
            dados = json.loads(arquivo_json.read())
            for data in dados[0]['relatorios']:
                data['Data'] = datetime.datetime.fromtimestamp(data['Data'] / 1e3)
            return dados

    except Exception as e:
        if str(e) == 'Expecting value: line 1 column 1 (char 0)':
            alertas.append({"titulo": "Alerta de Teste", "mensagem": e})
            return json.loads('[{"relatorios": []}]')



