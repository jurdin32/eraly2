from django.db import models

# Create your models here.
from Personas.models import UsuariosWeb
from Producto.models import Productos
from eraly2.snippers import ResizeImageMixin


class Publicidad(models.Model,ResizeImageMixin):
    imagen=models.ImageField(upload_to="imagenes")
    estado=models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.resize(self.imagen, (600, 800))
        super(Publicidad, self).save()

class ComprasWeb(models.Model):
    fecha=models.DateTimeField(auto_now_add=True)
    usuario=models.ForeignKey(UsuariosWeb,on_delete=models.CASCADE)
    subtotal=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    por_confirmar=models.BooleanField(default=True)
    hash=models.CharField(max_length=1000,null=True,blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.iva =float(self.total)*0.12
        self.subtotal=float(self.total) -float(self.iva)
        super(ComprasWeb, self).save()

    def __str__(self):
        return self.hash

class DetalleCompraWeb(models.Model):
    compra=models.ForeignKey(ComprasWeb, on_delete=models.CASCADE)
    producto=models.ForeignKey(Productos,on_delete=models.CASCADE)
    color=models.CharField(max_length=60,null=True,blank=True)
    precio_normal=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descuento_porcentaje=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    precio_promocion= models.DecimalField(max_digits=9, decimal_places=2, default=0)
    cantidad=models.IntegerField(default=0)
    precio_total= models.DecimalField(max_digits=9, decimal_places=2, default=0)
