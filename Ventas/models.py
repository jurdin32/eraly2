from django.db import models

# Create your models here.
from Empresa.models import Establecimiento
from Personas.models import Clientes
from Producto.models import Productos, Kardex


class Facturas(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, default="F")
    numero = models.CharField(max_length=20, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2)
    iva = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    estado=models.CharField(max_length=1, default="E")


class DetalleFactura(models.Model):
    fecha = models.DateField(auto_now_add=True, null=True, blank=True)
    factura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    precioU = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2)
    iva = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.iva = float(self.subtotal) * 0.12
        self.total = float(self.subtotal) + float(self.iva)

        if self.factura.tipo == "F":
            Kardex(producto=self.producto, tipo="E", cantidad=self.cantidad,
                   descripcion="Registrado segun factura de compra No. %s" % (self.factura.numero)).save()
        super(DetalleFactura, self).save()


class CuentasCobrar(models.Model):
    fecha=models.DateField(auto_now_add=True)
    factura_numero=models.CharField(max_length=20,null=True,blank=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2,default=0)

class Recibos(models.Model):
    fecha= models.DateField(auto_now_add=True)
    cuenta= models.ForeignKey(CuentasCobrar,on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2,default=0)
    formaPago = models.CharField(max_length=20)
    numeroCheque = models.CharField(max_length=20, null=True,blank=True)
    rebidoPor =models.CharField(max_length=60)
    recibiDe = models.CharField(max_length=60)