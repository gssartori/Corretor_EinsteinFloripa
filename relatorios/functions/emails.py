from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from relatorios.functions.utils import edita_status, alertas


_email_origem ='teste.einstein1@gmail.com'
_password = 'Molotov123'

# Configurando a sessão de login pelo protocolo SMTP
session = SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(_email_origem, _password)

def logout_email():
    # Após o último relatório a ser enviado, é preciso encerrar a sessão do email
    session.quit()


def envia_email(texto, email_destino):
    try:
        session.sendmail(_email_origem, email_destino, texto)
    except:
        try:
            # verificar erros, se o erro for session disconected:
            session.sendmail(_email_origem, email_destino, texto)
            # se for outro erro, fazer outra coisa:
        except Exception as e:
            print('???MOTIVO DO ERRO???::: ', e)
            return False
    return True

def constroi_email(pdf_aluno, nome_aluno, email_destino, assunto_mensagem = 'Relatório Simulinho'):
    print(f'Enviando relatório de: {nome_aluno} para {email_destino}')
    edita_status(nome_aluno, 'Enviando')

    corpo_texto = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla efficitur dictum tincidunt. 
    Nullam elementum non velit sed convallis. Quisque feugiat nec risus eget eleifend. 
    Proin bibendum metus congue diam vulputate venenatis. Nam aliquam urna sed nibh laoreet posuere. 
    Aliquam porta quam eget velit rutrum, nec tempus metus pharetra. 
    Orci varius natoque penatibus et magnis dis parturient montes, 
    nascetur ridiculus mus. Aliquam erat volutpat.
    '''

    # Atribuindo parâmetros da mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = _email_origem
    mensagem['To'] = email_destino
    mensagem['Subject'] = assunto_mensagem

    mensagem.attach(MIMEText(corpo_texto, 'plain'))

    # Criando o relatório a ser enviado
    payload = MIMEBase('application', 'octate-stream', Name = nome_aluno+'.pdf') #payload = MIMEBase('application', 'pdf', Name=pdfname)
    payload.set_payload((pdf_aluno))

    # codificando o relatório do formato binário para base64
    encoders.encode_base64(payload)

    # Título do PDF
    payload.add_header('Content-Decomposition', 'attachment', filename=nome_aluno+'.pdf')
    mensagem.attach(payload)

    envio_confirmado = envia_email(mensagem.as_string(), email_destino)
    edita_status(nome_aluno, 'Enviado',envio_confirmado)
    if envio_confirmado:
        print(f'!!!ENVIADO!!!: {nome_aluno} para {email_destino}')
    else:
        print(f'!!!NÃO ENVIADO!!!: {nome_aluno} !!!ERROR!!!')