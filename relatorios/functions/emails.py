from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

email_origem ='teste.einstein1@gmail.com'
password = 'Molotov123'

# Configurando a sessão de login pelo protocolo SMTP
session = None

def login_email():
    session = SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(email_origem, password)

def logout_email():
    # Após o último relatório a ser enviado, é preciso encerrar a sessão do email
    session.quit()

def envia_email(texto, email_destino):
    try:
        session.sendmail(email_origem, email_destino, texto)
    except:
        # verificar erros, se o erro for session disconected:
        login_email()
        session.sendmail(email_origem, email_destino, texto)
        # se for outro erro, fazer outra coisa:

def constroi_email(pdf_aluno, nome_aluno, email_destino, assunto_mensagem = 'Relatório Simulinho'):
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
    mensagem['From'] = email_origem
    mensagem['To'] = email_destino
    mensagem['Subject'] = assunto_mensagem

    mensagem.attach(MIMEText(corpo_texto, 'plain'))

    # Criando o relatório a ser enviado
    payload = MIMEBase('application', 'octate-stream', Name = nome_aluno) #payload = MIMEBase('application', 'pdf', Name=pdfname)
    payload.set_payload((pdf_aluno))

    # codificando o relatório do formato binário para base64
    encoders.encode_base64(payload)

    # Título do PDF
    payload.add_header('Content-Decomposition', 'attachment', filename=nome_aluno)
    mensagem.attach(payload)

    envia_email(mensagem.as_string(), email_destino)