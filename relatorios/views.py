from django.shortcuts import render
from .models import Relatorio, NovoStorage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from relatorios.functions import utils
from relatorios.functions.corretor_simulinho import cria_simulados


def index(request):
    # relatorios = Relatorio.objects.all()
    dados = dict() # {'relatorios': relatorios}
    utils.alertas.clear()

    if request.method == 'POST':
        arquivos_permitidos = ['acertos_aluno.pkl', 'colocacao.pkl', 'comentarios.pkl', 'dados_redacao.pkl', 'data.pkl', 'notas.pkl']
        arquivos_recebidos = request.FILES.getlist('dados_simulinho')

        if sorted([arquivo.name for arquivo in arquivos_recebidos]) == sorted(arquivos_permitidos):
            for arquivo in arquivos_recebidos:
                NovoStorage().save(arquivo.name, arquivo)
            utils.memo.clear()
            utils.cria_json()
            # if 'dados_simulinho' in request.FILES else False
            #     arquivo_armazenado = NovoStorage()
            #     arquivo_armazenado.save(arquivo_recebido.name, arquivo_recebido)
            #     if arquivo_recebido:
            #         utils.escreve_arquivo(arquivo_recebido)
            #         utils.memo.clear()

        return HttpResponseRedirect(reverse('index'))

    dados['relatorios'] = utils.le_arquivo()[0]['relatorios']
    if utils.alertas:
        dados['alertas'] = utils.alertas
    # dados.setdefault("url", []).append(NovoStorage().url(nome_arquivo))
    return render(request, 'index.html', dados)

def status_relatorios_ajax(request):
    novos_status = utils.novo_status.copy()
    utils.novo_status.clear()
    return JsonResponse({'novos_status': novos_status})
    # return render(request, 'index.html', utils.le_arquivo()[0])


def envia_relatorios(request):
    cria_simulados()
    return HttpResponseRedirect(reverse('index'))


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
