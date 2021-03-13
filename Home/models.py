from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from Empresa.models import Establecimiento


class Pais(models.Model):
    nombre=models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    pais=models.ForeignKey(Pais,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    provincia=models.ForeignKey(Provincia,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class ConfigurarDocumentos(models.Model):
    establecimiento = models.ForeignKey(Establecimiento,null=True,blank=True)
    proformas= models.IntegerField(default=1)
    facturas=models.IntegerField(default=1)

