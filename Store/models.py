from django.db import models

# Create your models here.
class Publicidad(models.Model):
    imagen=models.ImageField(upload_to="publicidad")
    estado=models.BooleanField(default=True)
