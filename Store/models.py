from django.db import models

# Create your models here.
from Personas.models import UsuariosWeb
from Producto.models import Productos, Precios
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
        self.iva =float(self.subtotal)*0.12
        self.total=float(self.subtotal) + float(self.iva)
        super(ComprasWeb, self).save()

    def __str__(self):
        return self.hash

class DetalleCompraWeb(models.Model):
    compra=models.ForeignKey(ComprasWeb, on_delete=models.CASCADE)
    producto=models.ForeignKey(Productos,on_delete=models.CASCADE)
    color=models.CharField(max_length=60,null=True,blank=True)
    talla=models.CharField(max_length=60,null=True,blank=True)
    precio_normal=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descuento_porcentaje=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    precio_promocion= models.DecimalField(max_digits=9, decimal_places=2, default=0)
    cantidad=models.IntegerField(default=0)
    precio_total= models.DecimalField(max_digits=9, decimal_places=2, default=0)
    autorizado=models.BooleanField(default=False)
    enviado=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    etiqueta=models.CharField(max_length=100,null=True,blank=True)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.etiqueta=str.upper(self.compra.hash[5:15])
        print(self.etiqueta)
        super(DetalleCompraWeb, self).save()

class Favoritos(models.Model):
    usuario=models.ForeignKey(UsuariosWeb,on_delete=models.CASCADE)
    producto =models.ForeignKey(Productos,on_delete=models.CASCADE)
    precio =models.DecimalField(default=0, max_digits=9, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        precios= Precios.objects.filter(producto=self.producto,web=True).last()
        self.precio=precios.precioVenta
        super(Favoritos, self).save()
