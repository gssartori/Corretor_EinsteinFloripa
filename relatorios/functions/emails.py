from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from relatorios.functions.utils import edita_status, alertas


_email_origem = 'teste.einstein1@gmail.com'
_password = 'Molotov123'

try:
    # Configurando a sessão de login pelo protocolo SMTP
    session = SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(_email_origem, _password)
except Exception as e:
    print(f"PDF não enviado. Erro: \n {e}")
    alertas.append({"titulo": f"PDF não enviado",
                    "mensagem": "Certifique-se que a opção de 'Acesso a app menos seguro' "
                                "está ativada para sua conta.\n Para saber mais:"
                                "\n https://support.google.com/accounts/answer/6010255"
                                "\n\n Caso esteja ativada, talvez a sessão esteja sendo "
                                "bloqueada por algum outro protocolo de segurança no acesso. "
                                "Verifique a aba de segurança da sua conta"})

def logout_email():
    # Após o último relatório a ser enviado, é preciso encerrar a sessão do email
    try: session.quit()
    except: pass


def envia_email(texto, email_destino):
    try:
        session.sendmail(_email_origem, email_destino, texto)
    except Exception as e:
        print('Email não enviado: \n', e)
        alertas.append({"titulo": f"PDF não enviado",
                        "mensagem": "Certifique-se que a opção de 'Acesso a app menos seguro' "
                                    "está ativada para sua conta.\n Para saber mais:"
                                    "\n https://support.google.com/accounts/answer/6010255"})
        return False
    return True

def constroi_email(pdf_aluno, nome_aluno, email_destino, assunto_mensagem = 'Relatório Simulinho'):
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

    # Codificando o relatório do formato binário para base64
    encoders.encode_base64(payload)

    # Título do PDF
    payload.add_header('Content-Decomposition', 'attachment', filename=nome_aluno+'.pdf')
    mensagem.attach(payload)

    envio_confirmado = envia_email(mensagem.as_string(), email_destino)

    if envio_confirmado:
        edita_status(nome_aluno, 'Enviado')
        print(f'!!!ENVIADO!!!: {nome_aluno} para {email_destino}')
    else:
        edita_status(nome_aluno, 'Não Enviado')
        print(f'!!!NÃO ENVIADO!!!: {nome_aluno}')