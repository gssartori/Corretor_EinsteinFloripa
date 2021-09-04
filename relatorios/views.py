from django.shortcuts import render
from .models import Relatorio, NovoStorage
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    relatorios = Relatorio.objects.all()
    dados = {'relatorios': relatorios}

    if request.method == 'POST':
        arquivo_recebido = request.FILES['planilha']
        arquivo_armazenado = NovoStorage()
        nome_arquivo = arquivo_armazenado.save(arquivo_recebido.name, arquivo_recebido)
        dados['url'] = arquivo_armazenado.url(nome_arquivo)
    return render(request, 'index.html', dados)