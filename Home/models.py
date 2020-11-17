from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from uuslug import uuslug as slugify


class Usuario(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    nombreCompleto=models.CharField(max_length=60)
    nombreComercial=models.CharField(max_length=70)

    def __str__(self):
        return "%s | %s: %s"%(self.nombreCompleto,self.user.username,self.nombreComercial)

class Tienda(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CharField)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    descripcion=RichTextUploadingField(null=True,blank=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.usuario.nombreComercial, instance=self)
        super(Tienda, self).save(*args, **kwargs)

class Direccion(models.Model):
    tienda=models.ForeignKey(Tienda,on_delete=models.CASCADE,null=True)
    direccion = models.CharField(max_length=60,null=True)
    telefono = models.CharField(max_length=10,blank=True)