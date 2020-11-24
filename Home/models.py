from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Pais(models.Model):
    nombre=models.CharField(max_length=60)

class Provincia(models.Model):
    pais=models.ForeignKey(Pais,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=60)

class Ciudad(models.Model):
    provincia=models.ForeignKey(Provincia,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)

class Usuario(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    nombreCompleto=models.CharField(max_length=60)
    nombreComercial=models.CharField(max_length=70)

    def __str__(self):
        return "%s | %s: %s"%(self.nombreCompleto,self.user.username,self.nombreComercial)