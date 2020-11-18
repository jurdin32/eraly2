from django.db import models

# Create your models here.
from Home.models import Ciudad, Direccion


class Proveedor(models.Model):
    ruc=models.CharField(max_length=10)
    nombreComercial=models.CharField(max_length=60)
    ciudad=models.ForeignKey(Ciudad,on_delete=models.CASCADE,null=True,blank=True)
    direccion=models.ForeignKey(Direccion,on_delete=models.CASCADE,null=True,blank=True)