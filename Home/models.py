from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Usuario(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    nombreCompleto=models.CharField(max_length=60)
    nombreComercial=models.CharField(max_length=70)

class Direccion(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE)
    direccion = models.CharField(max_length=60,null=True)
    telefono = models.CharField(max_length=10,blank=True)



