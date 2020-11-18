from django.db import models

# Create your models here.
from Home.models import Ciudad

class DireccionProveedor(models.Model):
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    direccion=models.CharField(max_length=60)
    telefono=models.CharField(max_length=10)

class Proveedor(models.Model):
    ruc=models.CharField(max_length=10)
    nombreComercial=models.CharField(max_length=60)
    direccion=models.ForeignKey(DireccionProveedor,on_delete=models.CASCADE,null=True,blank=True)