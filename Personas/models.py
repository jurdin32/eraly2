from django.db import models

# Create your models here.
from Home.models import Ciudad


class Clientes(models.Model):
    cedula=models.CharField(max_length=13)
    nombres=models.CharField(max_length=60)
    apellidos=models.CharField(max_length=60)
    direccion=models.CharField(max_length=60)
    ciudad=models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    telefono=models.CharField(max_length=13)
    celular=models.CharField(max_length=13)