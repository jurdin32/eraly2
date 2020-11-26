from django.contrib import admin

# Register your models here.
from Producto.models import *
from eraly2.snippers import Attr

@admin.register(TipoProveedor)
class AdminTipoProveedor(admin.ModelAdmin):
    list_display = Attr(TipoProveedor)
    list_display_links = Attr(TipoProveedor)


@admin.register(ActividadProveedor)
class AdminActividadProveedor(admin.ModelAdmin):
    list_display = Attr(ActividadProveedor)
    list_display_links = Attr(ActividadProveedor)



class DireccionInline(admin.StackedInline):
    model = DireccionProveedor
    extra = 0

@admin.register(Proveedor)
class AdminProveedor(admin.ModelAdmin):
    list_display = Attr(Proveedor)
    list_display_links = Attr(Proveedor)
    inlines = [DireccionInline]


@admin.register(Categorias)
class AdminCategorias(admin.ModelAdmin):
    list_display = Attr(Categorias)
    list_display_links = Attr(Categorias)

@admin.register(Subcategorias)
class AdminSubcategorias(admin.ModelAdmin):
    list_display = Attr(Subcategorias)
    list_display_links = Attr(Subcategorias)

@admin.register(DetallesProducto)
class AdminDetallesProducto(admin.ModelAdmin):
    list_display = Attr(DetallesProducto)
    list_display_links = Attr(DetallesProducto)

@admin.register(Productos)
class AdminProductos(admin.ModelAdmin):
    list_display = Attr(Productos)
    list_display_links = Attr(Productos)

@admin.register(Colores)
class AdminColores(admin.ModelAdmin):
    list_display = Attr(Colores)
    list_display_links = Attr(Colores)

@admin.register(Precios)
class AdminPrecios(admin.ModelAdmin):
    list_display = Attr(Precios)
    list_display_links = Attr(Precios)

@admin.register(Kardex)
class AdminKardex(admin.ModelAdmin):
    list_display = Attr(Kardex)
    list_display_links = Attr(Kardex)

@admin.register(ImagenesProducto)
class AdminImagenesProducto(admin.ModelAdmin):
    list_display = Attr(ImagenesProducto)
    list_display_links = Attr(ImagenesProducto)

@admin.register(DireccionProveedor)
class AdminDireccion(admin.ModelAdmin):
    list_display = Attr(DireccionProveedor)
    list_display_links = Attr(DireccionProveedor)
