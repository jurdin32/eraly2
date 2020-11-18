from django.db import models

# Create your models here.
from Home.models import Ciudad

class Proveedor(models.Model):
    ruc=models.CharField(max_length=10)
    nombreComercial=models.CharField(max_length=60)

class DireccionProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    direccion=models.CharField(max_length=60)
    telefono=models.CharField(max_length=10)