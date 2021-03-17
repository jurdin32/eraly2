from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from uuslug import uuslug as slugify

# Create your models here.
from Home.models import Ciudad


class Establecimiento(models.Model):
    logo=models.ImageField(upload_to="logos/establecimientos",null=True,blank=True)
    banner=models.ImageField(upload_to="banner/establecimientos",null=True,blank=True)
    pie_pagina=models.ImageField(upload_to="pie/establecimientos",null=True,blank=True)
    cabecera_tienda=models.ImageField(upload_to="logos/tienda",null=True,blank=True)
    color_encabezado_documentos=models.CharField(max_length=40, default="#ffffff")
    usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    ruc=models.CharField(max_length=13)
    nombreComercial=models.CharField(max_length=60)
    representateLegal=models.CharField(max_length=60)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    descripcion = RichTextUploadingField(null=True, blank=True)

    ubicacion_gps = models.CharField(max_length=300,null=True,blank=True)
    correo_electronico=models.EmailField(max_length=600,null=True,blank=True)
    web=models.CharField(max_length=400,null=True,blank=True)
    facebook=models.CharField(max_length=400,null=True,blank=True)
    instagram=models.CharField(max_length=400, null=True, blank=True)
    youtube = models.CharField(max_length=400,null=True,blank=True)

    def previa(self):
        return mark_safe('<a href="/admin/Empresa/establecimiento/%s/change/"><img src="/media/%s" style="width: 50px" alt=""></a>'%(self.id,self.logo))

    def __str__(self):
        if self.nombreComercial:
            return self.nombreComercial
        else:
            return self.representateLegal

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombreComercial, instance=self)
        super(Establecimiento, self).save(*args, **kwargs)


class ConfigurarDocumentos(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)
    proformas = models.IntegerField(default=1)
    facturas = models.IntegerField(default=1)


class Direccion(models.Model):
    establecimiento=models.ForeignKey(Establecimiento,on_delete=models.CASCADE,null=True)
    ciudad=models.ForeignKey(Ciudad,on_delete=models.CASCADE,null=True,blank=True)
    direccion = models.CharField(max_length=60,null=True)
    telefono = models.CharField(max_length=10,blank=True)

    def __str__(self):
        return mark_safe("<strong>Ciudad:</strong> %s <br><br><strong>Dirección:</strong> %s <br><br> <strong>Teléfono:</strong> %s"%(self.ciudad.nombre,self.direccion,self.telefono))


class UsuarioEmpresa(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombreCompleto=models.CharField(max_length=60)
    cedula=models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return "%s | %s: %s"%(self.nombreCompleto,self.user.username,self.nombreCompleto)