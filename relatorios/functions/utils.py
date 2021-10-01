# O arquivo utils.py contém os métodos e funções necessárias para o gerenciamento
# direto dos arquivos utilizados

from django.core.files.storage import default_storage
import pandas as pd
import json, datetime


alertas = []        # lista de dicionários
memo = {}           # memorizador do status_envio.json {'nome_aluno': index}
novo_status = []    # lista de dict's temporária que armazenam o nome e o novo status do aluno

def escreve_arquivo(relatorios):
    """ Função responsável por escrever algo no arquivo status_envio.json """
    try:
        with default_storage.open('status_envio.json', mode='w') as arquivo_json:
            json.dump([{"relatorios": json.loads(relatorios)}], arquivo_json, ensure_ascii=False)

    except Exception as e:
        alertas.append({"titulo": "Arquivo Não Identificado", "mensagem": e})  # dispara_alerta("Arquivo Corrompido", e)


def le_arquivo():
    """ Função responsável por ler o arquivo status_envio.json """
    try:
        with default_storage.open('status_envio.json', mode='r') as arquivo_json:
            return json.loads(arquivo_json.read())
            # for data in dados[0]['relatorios']: data['Data'] = datetime.datetime.fromtimestamp(data['Data'] / 1e3)
    except Exception as e:
        print('SE LIGA NO ERRO::::: ', e)
        alertas.append({"titulo": "Arquivo não lido", "mensagem": e})  # dispara_alerta("Arquivo Corrompido", e)
        return json.loads('[{"relatorios": []}]')


def edita_status(nome_aluno, proximo_status, envio_confirmado=True):
    """
      Método responsável por buscar e alterar o estado do relatório do aluno pelo seu nome;
      A busca realizada é do tipo binária, e é delimitada aos alunos cujos estados são
      diferentes de 'Enviado' / 'Enviando'

      Obs: o status_envio.json é ordenado pelo 'Status' e 'Nome' do aluno, respectivamente.
    """
    dados_aluno = le_arquivo()[0]['relatorios']
    if not envio_confirmado:
        proximo_status = 'Não Enviado'
        alertas.append({"titulo": "Error", "mensagem": "Email não enviado"})
    encontrou = False

    if nome_aluno in memo:
        index = memo[nome_aluno]
        dados_aluno[index]['Status'] = proximo_status
        encontrou = True

    else:
        for i, aluno in enumerate(dados_aluno):
            if (aluno['Nome'].lower() == nome_aluno.lower()):
                aluno["Status"] = proximo_status
                encontrou = True
                memo[nome_aluno] = i
                break
    if not encontrou:
        alertas.append({"titulo": "ERRO", "mensagem": "<-- Aluno não encontrado no JSON -->"})
    else:
        dados_editados = json.dumps(dados_aluno)
        escreve_arquivo(dados_editados)
        print(f'Status de "{dados_aluno[memo[nome_aluno]]["Status"]}" alterado')
        # adicionando o status atualizado para leitura do status_relatorios_ajax
        novo_status.append({nome_aluno: dados_aluno[memo[nome_aluno]]['Status']})



def procura_email(nome_aluno):
    """
    Essa função deve buscar o email do aluno de acordo com o nome_aluno.

    Uma possibilidade é upar um arquivo junto com os arquivos selecionados
    contendo o nome e o email do aluno. A busca pode ser feita com qualquer lib,
    e para acessar o diretório das medias basta verificar na função 'le_arquivo()'
    """
    return 'gabriel.s@autojun.com.br'


def cria_json():
    """
    Esse método é chamado apenas quando os dados .pkl são salvos, recebendo
    :return:
    """
    df_q = pd.read_pickle(default_storage.open('data.pkl'))
    dados_alunos = []
    for index, nome_aluno in enumerate(df_q.index.get_level_values(0).unique()):
        dados_alunos.append({'Nome': nome_aluno,
                             'Status': 'Pendente',
                             'Data': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                             'email': procura_email(nome_aluno)})
        memo[nome_aluno]: index

    escreve_arquivo(json.dumps(dados_alunos))



