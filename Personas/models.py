from django.db import models

# Create your models here.
from Empresa.models import Establecimiento
from Home.models import Ciudad


class Clientes(models.Model):
    establecimiento=models.ForeignKey(Establecimiento, on_delete=models.CASCADE,null=True,blank=True)
    cedula=models.CharField(max_length=13)
    nombres=models.CharField(max_length=60)
    apellidos=models.CharField(max_length=60)
    direccion=models.CharField(max_length=60)
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    telefono=models.CharField(max_length=13,null=True,blank=True)
    celular=models.CharField(max_length=13,null=True,blank=True)
    estado=models.BooleanField(default=True)

    def __str__(self):
        return "%s %s [%s]"%(self.nombres, self.apellidos, self.cedula)