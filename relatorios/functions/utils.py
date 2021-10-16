# O arquivo utils.py contém os métodos e funções necessárias para o gerenciamento
# dos arquivos utilizados, controle dos status de envio e alertas ao usuário

from django.core.files.storage import default_storage
import pandas as pd
import json, datetime
# from _pickle import dump

arquivos_permitidos = ['acertos_aluno.pkl', 'colocacao.pkl', 'comentarios.pkl', 'dados_redacao.pkl', 'data.pkl', 'notas.pkl']

novo_status = []    # [{'nome_aluno': "", 'novo_status_aluno': ""},]    Lista de status que preenche a tabela da página inicial
memo = {}           # {'nome_aluno': index}

def trata_alerta(alerta):
    """
        Função verifica os alertas já existentes em 'alertas.json, adiciona o
        novo alerta e os envia ao método 'escreve_arquivo()'
    """
    escreve_arquivo(alertas=json.dumps(le_arquivo('alertas')+[alerta]))


def verifica_dados():
    """
        Verifica se ocorreram mudanças nos alertas ou nos status dos alunos.
        Caso existam, as retorna para aparecer na tela inicial
    """
    dados = dict()
    global novo_status
    if novo_status:
        dados['novos_status'], novo_status = novo_status[:], []

    alertas = le_arquivo('alertas') #.setDefault('alertas', None)
    if alertas:
        dados['alertas'] = alertas.copy()
        escreve_arquivo(alertas=json.dumps([]))

    return dados


def valida_nome_uploads(nomes_arquivos_recebidos):
    """
    Função verifica se os arquivos recebidos estão nomeados corretamente

    :return:
    True se os nomes dos arquivos recebidos estão corretos,
    False caso contrário, adicionando uma mensagem de alerta ao usuário
    """
    if nomes_arquivos_recebidos == sorted(arquivos_permitidos):
        return True

    trata_alerta({"titulo": "!!!Atenção!!!",
                  "mensagem": f"Os {len(arquivos_permitidos)} uploads devem ter os seguintes nomes: "
                                f"\n\n{', '.join(arquivos_permitidos)}"})
    return False



def escreve_arquivo(relatorios=None, alertas=None):
    """ Função edita um dos arquivos .json da aplicação """
    try:
        arquivo = ('relatorios',relatorios) if relatorios else ('alertas',alertas)
        with default_storage.open(f'{arquivo[0]}.json', mode='w') as arquivo_json:
            json.dump([{arquivo[0]: json.loads(arquivo[1])}], arquivo_json, ensure_ascii=False)

    except Exception as e:
        escreve_arquivo(alertas=json.dumps([{"titulo": "Arquivo Não Identificado", "mensagem": str(e)}]))


def le_arquivo(arquivo):
    """ Função lê um dos arquivos .json """
    try:
        with default_storage.open(f'{arquivo}.json', mode='r') as arquivo_json:
            dados = json.loads(arquivo_json.read())[0][arquivo]
            if dados:
                return dados

    except Exception as e:
        escreve_arquivo(alertas=json.dumps([{"titulo": f"Arquivo '{arquivo}' não pode ser lido", "mensagem": str(e)}]))
    return json.loads('[]')


def edita_status(nome_aluno, proximo_status):
    """ Método busca e altera o status do aluno pelo seu nome """

    dados_aluno = le_arquivo('relatorios')
    status_alterado = False

    if nome_aluno in memo:
        dados_aluno[memo[nome_aluno]]['Status'] = proximo_status
        status_alterado = True
    else:
        for i, aluno in enumerate(dados_aluno):
            if (aluno['Nome'].lower() == nome_aluno.lower()):
                aluno["Status"] = proximo_status
                status_alterado = True
                memo[nome_aluno] = i
                break

    if status_alterado:
        dados_editados = json.dumps(dados_aluno)
        escreve_arquivo(relatorios=dados_editados)
        novo_status.append({nome_aluno: dados_aluno[memo[nome_aluno]]['Status']})
    else:
        trata_alerta({"titulo": f"Aluno {nome_aluno} não encontrado",
                      "mensagem": "Verifique se os arquivos carregados estão corrompidos"})


def procura_email(nome_aluno):
    """
    Essa função deve buscar o email do aluno de acordo com o nome_aluno.

    Uma possibilidade é upar um arquivo junto com os arquivos selecionados
    contendo o nome e o email do aluno. A busca pode ser feita com qualquer lib,
    e para acessar o diretório das medias basta verificar na função 'le_arquivo()'

    Obs: A variável 'arquivos_permitidos' deve ser alterada na ocorrência de
    qualquer mudança na quantidade e nome dos arquivos enviados ao servidor.
    """
    return 'gabriel.s@autojun.com.br'


def cria_json():
    """ Esse método é chamado apenas quando os arquivos .pkl são upados e salvos. """
    df_q = pd.read_pickle(default_storage.open('data.pkl'))
    dados_alunos = []

    for index, nome_aluno in enumerate(df_q.index.get_level_values(0).unique()):
        dados_alunos.append({'Nome': nome_aluno,
                             'Status': 'Pendente',
                             'Data': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                             'email': procura_email(nome_aluno)})
        memo[nome_aluno]: index

    escreve_arquivo(relatorios=json.dumps(dados_alunos))


def limpa_dados():
    """ Método limpa todas as informações dos alunos no servidor. """
    # limpando os arquivos .pkl
    for arquivo in arquivos_permitidos:
        try:
            if arquivo.split('.')[-1] == 'pkl':
                with default_storage.open(f"{arquivo}", mode='w') as file:
                    json.dump([], file)
            # Caso existam outros arquivos de outros tipos, colocar aqui...

        except Exception as e:
            trata_alerta({"titulo": f"Arquivo {arquivo} Não Encontrado", "mensagem": e})

    # limpando arquivos .json
    escreve_arquivo(relatorios=json.dumps([]))
    escreve_arquivo(alertas=json.dumps([]))

