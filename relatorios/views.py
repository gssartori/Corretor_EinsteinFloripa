from django.shortcuts import render
from .models import Relatorio, NovoStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from relatorios.functions import utils


def index(request):
    # relatorios = Relatorio.objects.all()
    dados = dict() # {'relatorios': relatorios}
    utils.alertas.clear()

    if request.method == 'POST':
        arquivo_recebido = utils.converte_arquivo(request.FILES['planilha']) \
            if 'planilha' in request.FILES else False

        if arquivo_recebido:
            utils.escreve_arquivo(arquivo_recebido)
            utils.memo.clear()

        return HttpResponseRedirect(reverse('index'))

        # arquivo_armazenado = NovoStorage()
        # nome_arquivo = arquivo_armazenado.save('dados.json', arquivo_recebido)
        # arquivo_json = trata_arquivo(nome_arquivo)
        # dados['url'] = arquivo_armazenado.url(nome_arquivo)
    dados['relatorios'] = utils.le_arquivo()[0]['relatorios']
    if utils.alertas:
        dados['alertas'] = utils.alertas

    return render(request, 'index.html', dados)




# # PDF
# from django.template.loader import render_to_string
# # from weasyprint import HTML
# import tempfile
# from django.db.models import Sum
#
# def exporta_pdf():
#     pass
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename='+str("NOME_ALUNO")+'.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
#
#     dados = {}
#     html_string = render_to_string('templates/simulinho_aluno_template.html', dados)
#     html = HTML(string=html_string)
#
#     result = html.write_pdf()
#
#     with tempfile.NamedTemporaryFile(delete=True) as simulinho:
#         simulinho.write(result)
#         simulinho.flush()
#
#         output = open(simulinho.name, 'rb')
#         response.write(output.read())
#
#     return response
