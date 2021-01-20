from django.db import models

# Create your models here.
from Personas.models import Clientes
from Producto.models import Productos, Kardex


class Facturas(models.Model):
    tipo=models.CharField(max_length=20, default="F")
    fecha=models.DateField(auto_now_add=True)
    cliente=models.ForeignKey(Clientes,on_delete=models.CASCADE)
    subtotal=models.DecimalField(max_digits=9, decimal_places=2)
    iva=models.DecimalField(max_digits=9, decimal_places=2)
    total=models.DecimalField(max_digits=9, decimal_places=2)


class detalleFactura(models.Model):
    factura=models.ForeignKey(Facturas,on_delete=models.CASCADE)
    producto=models.ForeignKey(Productos,on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=0)
    subtotal=models.DecimalField(max_digits=9, decimal_places=2)
    iva = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.factura.tipo=="F":
            Kardex(producto=self.producto,tipo="E",cantidad=self.cantidad,descripcion="Registrado segun factura de compra No. %s"%(self.factura_id)).save()
        super(detalleFactura, self).save()
