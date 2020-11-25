from django.contrib import admin

# Register your models here.
from Producto.models import Proveedor, DireccionProveedor, Categorias, Subcategorias, DetallesProducto, Productos, \
    Colores, Precios, Kardex, ImagenesProducto
from eraly2.snippers import Attr

class DireccionInline(admin.StackedInline):
    model = DireccionProveedor
    extra = 0

@admin.register(Proveedor)
class AdminProveedor(admin.ModelAdmin):
    list_display = Attr(Proveedor)
    list_display_links = Attr(Proveedor)
    inlines = [DireccionInline]

@admin.register(Categorias)
class Categorias(admin.ModelAdmin):
    list_display = Attr(Categorias)
    list_display_links = Attr(Categorias)

@admin.register(Subcategorias)
class Subcategorias(admin.ModelAdmin):
    list_display = Attr(Subcategorias)
    list_display_links = Attr(Subcategorias)

@admin.register(DetallesProducto)
class DetallesProducto(admin.ModelAdmin):
    list_display = Attr(DetallesProducto)
    list_display_links = Attr(DetallesProducto)

@admin.register(Productos)
class Productos(admin.ModelAdmin):
    list_display = Attr(Productos)
    list_display_links = Attr(Productos)

@admin.register(Colores)
class Colores(admin.ModelAdmin):
    list_display = Attr(Colores)
    list_display_links = Attr(Colores)

@admin.register(Precios)
class Precios(admin.ModelAdmin):
    list_display = Attr(Precios)
    list_display_links = Attr(Precios)

@admin.register(Kardex)
class Kardex(admin.ModelAdmin):
    list_display = Attr(Kardex)
    list_display_links = Attr(Kardex)

@admin.register(ImagenesProducto)
class ImagenesProducto(admin.ModelAdmin):
    list_display = Attr(ImagenesProducto)
    list_display_links = Attr(ImagenesProducto)

@admin.register(DireccionProveedor)
class AdminDireccion(admin.ModelAdmin):
    list_display = Attr(DireccionProveedor)
    list_display_links = Attr(DireccionProveedor)
