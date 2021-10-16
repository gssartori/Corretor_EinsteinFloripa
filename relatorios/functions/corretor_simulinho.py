import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.core.files.storage import default_storage
from Corretor_EinsteinFloripa.relatorios.functions.utils import edita_status, procura_email, trata_alerta
from Corretor_EinsteinFloripa.relatorios.functions.emails import constroi_email, logout_email
# from jinja2 import Environment, FileSystemLoader
# from flask import url_for
# import numpy as np


# funções pra colorir as tabelas
def _color_correction(data):
    df = data.copy()
    df.loc[df['Sua resposta'] == df['Gabarito'], :] = 'background-color: lightgreen'
    df.loc[df['Sua resposta'] != df['Gabarito'], :] = 'background-color: #d48585'
    return df

def _color_table_every_other(data):
    df = data.copy()
    n = len(df)
    df.iloc[range(0, n, 2), :] = 'background-color: #f5f5dc'
    df.iloc[range(1, n, 2), :] = 'background-color: #f0f0ce'
    df.iloc[-1, :] += '; font-weight: bold'
    return df

def _color_table_redacao(data):
    df = data.copy()
    n = len(df)
    df.iloc[0:6, 0:3] = 'background-color: #f0f0ce'
    df.iloc[-1] += '; font-weight: bold'
    return df



def cria_simulados(nome_aluno = None, enviar_email = True):
    """
        Função responsável por preencher o template HTML com os dados dos alunos.

    :param nome_aluno:
        - Vazio por padrão, indicando que todos os PDFs serão criados e enviados por
    email automaticamente através da pasta 'emails'.
        - Se um nome for passado como parâmetro na chamada da função, será preenchido
    apenas o PDF do respectivo aluno

    :param enviar_email:
        Informa a função se o PDF criado deve ser ou não enviado via email
    """

    try:
        # carrega os DataFrames com os dados de questoes
        df_q = pd.read_pickle(default_storage.open('data.pkl'))
        df_q = df_q.rename(columns={'Resposta': 'Sua resposta', 'Gabarito': 'Gabarito'})
        df_q['Sua resposta'] = df_q['Sua resposta'].str.upper()
        df_q['Gabarito'] = df_q['Gabarito'].str.upper()

        # notas dos alunos por materia
        df_n = pd.read_pickle(default_storage.open('acertos_aluno.pkl'))
        df_n['Média Individual'] = df_n['Média Individual'].apply(lambda x: str(int(x * 100)) + '%')
        df_n['Media Geral'] = df_n['Media Geral'].apply(lambda x: str(int(x * 100)) + '%')

        # dados da redacao
        df_r = pd.read_pickle(default_storage.open('dados_redacao.pkl'))

        # colocação dos alunos
        colocacao = pd.read_pickle(default_storage.open('colocacao.pkl'))

        relatorio_alunos = {}

        # /!\ IMPORTANTE /!\
        # aqui carrega o template HTML que vai ser usado pelo Jinja
        template = get_template("simulinho_aluno_template.html")

        # cria um dicionário com as variáveis pro template
        doc = {'document_title': 'Correção SIMULINHO 2021'}

        emails_nao_enviados = 0
        # pra cada aluno
        for aluno in df_q.index.get_level_values(0).unique():
            if (nome_aluno == None or nome_aluno == aluno):
                edita_status(aluno, 'Gerando')

                # a cada iteração, ele pega os dados correspondente ao 'aluno'
                doc['nome'] = aluno  # nome do aluno
                doc['materias'] = []

                # colocacao de cada aluno
                coloc_aluno = colocacao[colocacao["Nome"] == aluno]

                coloc_aluno.loc[:, 'Colocação'] = coloc_aluno['Colocação']

                doc['colocacao'] = coloc_aluno.Colocação.iat[-1]

                # questoes de cada aluno
                df_q_aluno = df_q.loc[aluno, :]

                df_q_aluno['Questão'] = df_q_aluno.index.get_level_values(1)

                df_q_aluno = df_q_aluno[['Questão', 'Sua resposta', 'Gabarito', 'Assunto', 'Dificuldade']]

                # pra cada matéria:
                for materia in df_q_aluno.index.get_level_values(0).unique():
                    df_q_aluno_loc = df_q_aluno.loc[materia, :].style.apply(_color_correction, axis=None).set_properties(
                        **{'text-align': 'center',
                           'border-color': 'black',
                           'border-style': 'solid',
                           'border-width': '1px',
                           'border-collapse': 'collapse'}
                        # df_table_styles = df_q_aluno.style.set_table_styles([{'props': [('color', '#533884'), ('font-family', 'Roboto')]}])
                        # print(f'111111111111111111: {df_q_aluno_loc}')
                    ).hide_index().render()
                    doc['materias'].append({'materia': materia, 'df': df_q_aluno_loc})
                # mostrar a pontuação em cada materia

                df_n_aluno = df_n.loc[aluno, :]
                df_n_aluno['Matéria'] = df_n_aluno.index.get_level_values(0)
                df_n_aluno.loc[:, 'Total de Acertos'] = df_n_aluno['Total de Acertos']
                df_n_aluno.loc[:, 'Média Individual'] = df_n_aluno['Média Individual']
                df_n_aluno.loc[:, 'Media Geral'] = df_n_aluno['Media Geral']

                df_n_aluno = df_n_aluno[['Matéria', 'Total de Acertos', 'Média Individual', 'Media Geral']]

                doc['notas'] = df_n_aluno.style.apply(
                    _color_table_every_other,
                    axis=None
                ).set_properties(
                    **{'text-align': 'center',
                       'font-family': 'Roboto',
                       'border-color': 'black',
                       'border-style': 'solid',
                       'border-width': '1px',
                       'border-collapse': 'collapse'}
                    # ).set_table_styles(
                    #     [{'props': [('color', '#533884'), ('font-family', 'Roboto')]}]
                ).hide_index().render()

                # pode ser que alguns alunos façam a redação e não façam a prova objetiva, e vice-versa
                if aluno in df_r.index:
                    red_aluno = df_r.loc[aluno, :]

                    red_aluno["Critério"] = red_aluno.index.get_level_values(0)
                    red_aluno.loc[:, 'Nota'] = (red_aluno['Nota']).astype(str)
                    red_aluno.loc[:, 'Comentário'] = red_aluno['Comentário']

                    doc['comentario'] = red_aluno.Comentário.iat[-1]

                    red_aluno = red_aluno[['Critério', 'Nota']]

                    doc['redacao'] = red_aluno.style.apply(
                        _color_table_redacao,
                        axis=None
                    ).set_properties(
                        **{'text-align': 'center',
                           'font-family': 'Roboto',
                           'border-color': 'black',
                           'border-style': 'solid',
                           'border-width': '1px',
                           'border-collapse': 'collapse'}
                        # ).set_table_styles(
                        #     [{'props': [('color', '#533884'), ('font-family', 'Roboto')]}]
                    ).hide_index().render()

                else:
                    doc['redacao'] = ['Não fez a redação']
                    doc['comentario'] = []

                # renderiza o html a partir do template e com as informações do dicionário
                html_out = template.render(doc)
                html_para_pdf = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html_out.encode("UTF-8")), html_para_pdf, encoding='UTF-8')

                if not pdf.err:
                    if enviar_email:
                        envio_confirmado = constroi_email(html_para_pdf.getvalue(), doc['nome'], procura_email(aluno))

                        # Se 4 relatórios seguidos não forem enviados, o laço for se encerra
                        if envio_confirmado: emails_nao_enviados = 0
                        elif emails_nao_enviados >= 4: break
                        else: emails_nao_enviados += 1
                    else:
                        edita_status(aluno, 'Gerado')
                        return html_para_pdf.getvalue()
                else:
                    trata_alerta({"titulo": f"PDF de {aluno} não foi criado corretamente", "mensagem": pdf.err})
        logout_email()

    except:
        trata_alerta({"titulo": f"Arquivos não identificados ou corrompidos",
                      "mensagem": "Faça upload novamente de todos os arquivos necessários."})
