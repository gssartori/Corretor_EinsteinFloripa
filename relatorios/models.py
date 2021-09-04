from django.db import models
from datetime import datetime
from django.core.files.storage import FileSystemStorage

# Create your models here.

class Relatorio(models.Model):
    nome_aluno = models.CharField(max_length=255, primary_key=True, blank=False)
    email = models.CharField(max_length=255, blank=False)
    descricao_status = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    data_envio = models.DateTimeField(default=datetime.now, blank=True)


class NovoStorage(FileSystemStorage):
    def get_available_name(self, name, max_length):
        """
        Retorna um filename disponível para a class storage e
        o novo conteúdo para ser gravado
        """
        # Se o filename já existir, este é removido
        if self.exists(name):
            self.delete(name)
        return name