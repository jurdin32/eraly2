import datetime

from django.core.files import File
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

from Empresa.models import Establecimiento
from Home.models import Ciudad
from eraly2.snippers import ResizeImageMixin, Hash_parse

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
    nombre=models.CharField(max_length=200)
    descripcion=models.TextField(null=True,blank=True)
    slug=models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
        return '%s' % (self.nombre)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nombre=str.upper(self.nombre)
        self.slug = str.upper(self.slug)
        super(Categorias, self).save()

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
    nombre=models.CharField(max_length=200)


    def __str__(self):
        return '%s' % (self.nombre)

    class Meta:
        verbose_name_plural = "2. Subcategorias "

class Subcategorias_2(models.Model):
    subcategoria = models.ForeignKey(Subcategorias, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=200)

    def __str__(self):
        return '%s' % (self.nombre)

    class Meta:
        verbose_name_plural = "2.1 Subcategorias Subcategoría"

class Marca(models.Model):
    nombre=models.CharField(max_length=40)
    imagen=models.ImageField(upload_to="marca/imagenes",null=True,blank=True)

    def __str__(self):
        return self.nombre

class Productos(models.Model,ResizeImageMixin):
    tipo=models.CharField(max_length=20, default="P")
    imagen=models.ImageField(upload_to="productos",null=True,blank=True)
    codigo=models.CharField(max_length=300, null=True,blank=True, help_text="Solo si tiene codigo interno o codigo de barras")
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)
    subcategoria=models.ForeignKey(Subcategorias_2, on_delete=models.CASCADE,null=True,blank=True)
    marca=models.ForeignKey(Marca,on_delete=models.CASCADE,null=True,blank=True)
    nombre=models.CharField(max_length=100)
    talla=models.CharField(max_length=50,null=True,blank=True)
    dimension=models.CharField(max_length=200,null=True,blank=True)
    detallesTecnicos = RichTextUploadingField(null=True,blank=True,help_text="Es opcional",default="Sin detalles Técnicos")
    descripcion = RichTextUploadingField(default="Sin descripción",null=True,blank=True)
    estado=models.BooleanField(default=True)
    hash = models.CharField(max_length=256,null=True,blank=True)
    puntuacion=models.DecimalField(max_digits=9, decimal_places=2,default=0)
    etiquetas=models.TextField(default="",null=True,blank=True)

    def _descripcion(self):
        return mark_safe(self.descripcion)

    def _detallesTecnicos(self):
        return mark_safe(self.detallesTecnicos)

    def __str__(self):
        if self.talla:
            return '%s, talla:%s' % (self.nombre, self.talla)
        else:
            return '%s'%(self.nombre)

    def delete(self, using=None, keep_parents=False):
       storage, path = self.imagen.storage, self.imagen.path
       super(Productos, self).delete()
       storage.delete(path)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.tipo=="P" and not self.imagen:
            self.imagen = 'noproducto.png'

        if self.tipo=="S" and not self.imagen:
            self.imagen = 'noservicio.png'

        if self.tipo=="V" and not self.imagen:
            self.imagen = 'novehiculo.png'

        if self.tipo=="I" and not self.imagen:
            self.imagen = 'noinmueble.png'

        try:
            self.resize(self.imagen,(600,600))
        except:
            pass
        super(Productos, self).save()


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
    precioVenta=models.DecimalField(max_digits=9, decimal_places=2)
    iva=models.DecimalField(max_digits=9, decimal_places=2,default=0)
    total=models.DecimalField(max_digits=9, decimal_places=2,default=0)
    detalle=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)
    web=models.BooleanField(default=False)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.iva= float(self.precioVenta)*0.12
        self.total = float(self.iva) + float(self.precioVenta)
        
        super(Precios, self).save()

    def __str__(self):
        return "%s - %s"%(self.total, self.producto.nombre)


    class Meta:
        verbose_name_plural = "6. Precios Producto "

class Kardex(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    tipo=models.CharField(max_length=1)
    cantidad=models.IntegerField(default=0)
    descripcion=models.TextField()

    class Meta:
        verbose_name_plural = "7. Kardex "

    def __str__(self):
        return self.producto.nombre

class ImagenesProducto(models.Model,ResizeImageMixin):
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='productos', null=True, blank=True, help_text='600x800')
    thumbnail=models.ImageField(upload_to='productos/thumbnail', null=True, blank=True)

    def __str__(self):
        return '%s' % (self.producto_id)

    def miniatura(self):
        return mark_safe("<img src='/media/%s'>" % self.thumbnail)

    def delete(self, using=None, keep_parents=False):
       storage, path = self.imagen.storage, self.imagen.path
       super(ImagenesProducto, self).delete()
       storage.delete(path)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.resize(self.imagen, (600, 600))
        self.resize(self.thumbnail, (200, 200))
        super(ImagenesProducto, self).save()


    class Meta:
        verbose_name_plural = "8. Imagenes de Producto "

class CalificacionProductos(models.Model):
    usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    producto=models.ForeignKey(Productos,on_delete=models.CASCADE)
    rating=models.IntegerField(default=1)
    comentario=models.TextField(blank=True,null=True)


class Promociones(models.Model):
    fechaInicio=models.DateField()
    fechaFinal=models.DateField()
    precio =models.ForeignKey(Precios,on_delete=models.CASCADE)
    descuento =models.IntegerField(default=0)
    total =models.DecimalField(max_digits=9, decimal_places=2, default=0)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        precio= float(self.precio.precioVenta) - (float(self.precio.precioVenta) *float(self.descuento)/100)
        self.total =precio
        super(Promociones, self).save()



