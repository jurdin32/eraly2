from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

from Empresa.models import Establecimiento
from Home.models import Ciudad

contacto_chosse=(
    ('celular','celular'),('correo','correo'),('web','web')
)

tipo_proveedor_chosse=(
    ('productos/bienes','productos/bienes'),('servicios','servicios'),('recursos','recursos')
)

class Proveedor(models.Model):
    establecimiento=models.ForeignKey(Establecimiento,on_delete=models.CASCADE,null=True,blank=True)
    logo=models.ImageField(upload_to='proveedor', null=True, blank=True, help_text='100x100')
    ruc=models.CharField(max_length=13)
    nombre_fantasia=models.CharField(max_length=60,null=True,blank=True)
    representante=models.CharField(max_length=60,null=True,blank=True)

    def __str__(self):
        return self.nombre_fantasia

class TipoProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    detalle = models.CharField(choices=tipo_proveedor_chosse, max_length=30, null=True, blank=True)

    def __str__(self):
        return self.proveedor.nombre_fantasia

class ActividadProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=60)
    detalle = models.TextField()


class Categorias(models.Model):
    establecimiento=models.ForeignKey(Establecimiento,on_delete=models.CASCADE,null=True,blank=True)
    icono=models.CharField(max_length=20, default='fa fa-')
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)

    def __str__(self):
        return '%s' % (self.nombre)

    class Meta:
        verbose_name_plural = "1. Categorias "

class DireccionProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    direccion=models.CharField(max_length=60)
    telefono=models.CharField(max_length=60)

    def __str__(self):
        return "%s - %s: %s,  Telf.:%s"%(self.ciudad.nombre, self.ciudad.provincia.nombre, self.direccion,self.telefono)


class Subcategorias(models.Model):
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    icono=models.CharField(max_length=20)
    nombre=models.CharField(max_length=50)
    descripcion=models.TextField()


    def __str__(self):
        return '%s | %s' % (self.categoria.nombre,self.nombre)

    class Meta:
        verbose_name_plural = "2. Subcategorias "

class Marca(models.Model):
    nombre=models.CharField(max_length=40)
    imagen=models.ImageField(upload_to="marca/imagenes",null=True,blank=True)

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)
    subcategoria=models.ForeignKey(Subcategorias, on_delete=models.CASCADE)
    Marca=models.ForeignKey(Marca,on_delete=models.CASCADE,null=True,blank=True)
    nombre=models.CharField(max_length=100)
    talla=models.CharField(max_length=10,null=True,blank=True)
    dimension=models.CharField(max_length=200,null=True,blank=True)
    detallesTecnicos = RichTextUploadingField(null=True,blank=True,help_text="Es opcional")
    descripcion = RichTextUploadingField()
    estado=models.BooleanField(default=True)

    def __str__(self):
        return '%s'%(self.nombre)

    class Meta:
        verbose_name_plural = "3. Producto "


class DetallesProducto(models.Model):
    producto=models.ForeignKey(Productos,on_delete=models.CASCADE,null=True,blank=True)
    precioCompra=models.DecimalField(max_digits=9,decimal_places=2,default=0)
    iva=models.DecimalField(max_digits=9,decimal_places=4,default=0,help_text="Calculado automaticamente")
    pc=models.DecimalField(max_digits=9,decimal_places=4,default=0,help_text="Calculado automaticamente")

    def clean(self):
        self.iva=float(self.precioCompra)*0.12
        self.pc=float(self.precioCompra) + float(self.iva)

    def __str__(self):
        return '%s | %s'%(self.producto.nombre, self.pc)


    class Meta:
        verbose_name_plural = "4. Detalles del Producto "

class Colores(models.Model):
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=50)
    codigoColor=ColorField(default="#fff")

    def color(self):
        return mark_safe('<div style="background-color: %s; height: 30px; width: 100px"></div>'%self.codigoColor)

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
    descripcion=models.TextField()


    class Meta:
        verbose_name_plural = "7. Kardex "

class ImagenesProducto(models.Model):
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='producto', null=True, blank=True, help_text='100x100')

    def __str__(self):
        return '%s' % (self.producto_id)

    def miniatura(self):
        return mark_safe("<img src='/media/%s' style='width: 100px'>" % self.imagen)

    class Meta:
        verbose_name_plural = "8. Imagenes de Producto "



