from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

from Home.models import Ciudad

class Proveedor(models.Model):
    ruc=models.CharField(max_length=10)
    nombreComercial=models.CharField(max_length=60)

class DireccionProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    direccion=models.CharField(max_length=60)
    telefono=models.CharField(max_length=10)

class Categorias(models.Model):
    icono=models.CharField(max_length=10)
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)

    def __str__(self):
        return '%s' % (self.nombre)

    class Meta:
        verbose_name_plural = "1. Categorias "


class Subcategorias(models.Model):
    icono=models.CharField(max_length=10)
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
    categoria_id=models.ForeignKey(Categorias, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.categoria_id)

    class Meta:
        verbose_name_plural = "2. Subcategorias "

class Productos(models.Model):
    subcategoria=models.ForeignKey(Subcategorias, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=100)
    talla=models.CharField(max_length=10)
    dimension=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
    estado=models.CharField(max_length=50)

    def __str__(self):
        return '%s'%(self.nombre)

    class Meta:
        verbose_name_plural = "3. Producto "


class DetallesProducto(models.Model):
    producto=models.ForeignKey(Productos,on_delete=models.CASCADE,null=True,blank=True)
    precioCompra=models.DecimalField(max_digits=9,decimal_places=4,default=0)
    iva=models.DecimalField(max_digits=9,decimal_places=4,default=0)
    pc=models.DecimalField(max_digits=9,decimal_places=4,default=0)

    def __str__(self):
        return '%s | %s'%(self.producto.nombre, self.pc)


    class Meta:
        verbose_name_plural = "4. Detalles del Producto "

class Colores(models.Model):
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=50)
    codigoColor=models.CharField(max_length=50)

    def __str__(self):
        return '%s'%(self.nombre)

    class Meta:
        verbose_name_plural = "5. Color Producto "

class Precios(models.Model):
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    precioVenta=models.DecimalField(max_digits=5, decimal_places=2)
    detalle=models.CharField(max_length=50)


    class Meta:
        verbose_name_plural = "6. Precios Producto "

class Kardex(models.Model):
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    tipo=models.CharField(max_length=50)
    fecha=models.DateTimeField(auto_now = True)
    cantidad=models.IntegerField(default=0)
    descripcion=models.CharField(max_length=150)


    class Meta:
        verbose_name_plural = "7. Kardex "

class ImagenesProducto(models.Model):
    producto_id=models.ForeignKey(Productos, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='producto', null=True, blank=True, help_text='100x100')

    def __str__(self):
        return '%s' % (self.producto_id)

    def miniatura(self):
        return mark_safe("<img src='/media/%s' style='width: 100px'>" % self.imagen)

    class Meta:
        verbose_name_plural = "8. Imagenes de Producto "



