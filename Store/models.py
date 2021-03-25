from django.db import models

# Create your models here.
from eraly2.snippers import ResizeImageMixin


class Publicidad(models.Model,ResizeImageMixin):
    imagen=models.ImageField(upload_to="imagenes")
    estado=models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.resize(self.imagen, (600, 800))
        super(Publicidad, self).save()
