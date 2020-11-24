from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from uuslug import uuslug as slugify

# Create your models here.
from Home.models import Ciudad


class Establecimiento(models.Model):
    usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    ruc=models.CharField(max_length=13)
    nombreComercial=models.CharField(max_length=60)
    representateLegal=models.CharField(max_length=60)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    descripcion = RichTextUploadingField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombreComercial, instance=self)
        super(Establecimiento, self).save(*args, **kwargs)


class Direccion(models.Model):
    establecimiento=models.ForeignKey(Establecimiento,on_delete=models.CASCADE,null=True)
    ciudad=models.ForeignKey(Ciudad,on_delete=models.CASCADE,null=True,blank=True)
    direccion = models.CharField(max_length=60,null=True)
    telefono = models.CharField(max_length=10,blank=True)

    def __str__(self):
        return "%s|%s|%s"%(self.ciudad.nombre,self.direccion,self.telefono)


class UsuarioEmpresa(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombreCompleto=models.CharField(max_length=60)
    cedula=models.CharField(max_length=10,null=True,blank=True)

    # def __str__(self):
    #     return "%s | %s: %s"%(self.nombreCompleto,self.user.username,self.nombreCompleto)