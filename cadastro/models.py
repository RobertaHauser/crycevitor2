from django.db import models
from django.conf import settings

# Create your models here.
class Unidade(models.Model):
    nome = models.CharField(max_length=30, unique=True, verbose_name='Unidade', help_text="Não utilizar espaço",error_messages={'unique':"Este nome de Unidade dever ser único!"})
    sigla = models.CharField(max_length=3, unique=True, verbose_name='Sigla', help_text="03 letras",error_messages={'unique':"A sigla de Unidade dever ser única!"})
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name='Cadastro', blank=True)
    created_at= models.DateTimeField(auto_now_add=True, verbose_name='Data cadastro')
    edited_by= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', verbose_name='Revisão', null=True)
    edited_at= models.DateTimeField(auto_now=True, verbose_name='Data revisão',blank=True,null=True)

    def editado_por(self):
        is_datas_diferentes = self.created_at != self.edited_at
        print(self.nome, is_datas_diferentes)
        if is_datas_diferentes:
            return self.created_by.complete_name()
        return ""

    def editado_em(self):
        is_datas_diferentes = self.created_at != self.edited_at

        if is_datas_diferentes:
            return self.edited_at
        return ""

    class Meta:
        verbose_name="Unidade"
        verbose_name_plural="Unidades"
        db_table="unidade"

    def __str__(self):
        return self.nome