from django.contrib import admin

# Register your models here.
from django.forms import TextInput, Textarea, Select

from Producto.models import *
from eraly2.snippers import Attr


@admin.register(TipoProveedor)
class AdminTipoProveedor(admin.ModelAdmin):
    list_display = Attr(TipoProveedor)
    list_display_links = Attr(TipoProveedor)
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


@admin.register(ActividadProveedor)
class AdminActividadProveedor(admin.ModelAdmin):
    list_display = Attr(ActividadProveedor)
    list_display_links = Attr(ActividadProveedor)
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


class DireccionInline(admin.StackedInline):
    model = DireccionProveedor
    extra = 0


@admin.register(Proveedor)
class AdminProveedor(admin.ModelAdmin):
    list_display = Attr(Proveedor)
    list_display_links = Attr(Proveedor)
    inlines = [DireccionInline]
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


@admin.register(Categorias)
class AdminCategorias(admin.ModelAdmin):
    list_display = Attr(Categorias)
    list_display_links = Attr(Categorias)
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


@admin.register(Subcategorias)
class AdminSubcategorias(admin.ModelAdmin):
    list_display = Attr(Subcategorias)
    list_display_links = Attr(Subcategorias)
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


@admin.register(DetallesProducto)
class AdminDetallesProducto(admin.ModelAdmin):
    list_display = Attr(DetallesProducto)
    list_display_links = Attr(DetallesProducto)
    readonly_fields = ['iva','pc']
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


@admin.register(Marca)
class AdminMarca(admin.ModelAdmin):
    list_display = Attr(Marca)
    list_display_links = Attr(Marca)
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


@admin.register(Productos)
class AdminProductos(admin.ModelAdmin):
    list_display = Attr(Productos)
    list_display_links = Attr(Productos)
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:90%'})
        },
    }


@admin.register(Colores)
class AdminColores(admin.ModelAdmin):
    list_display = Attr(Colores)+['color']
    list_display_links = Attr(Colores)


@admin.register(Precios)
class AdminPrecios(admin.ModelAdmin):
    list_display = Attr(Precios)
    list_display_links = Attr(Precios)


@admin.register(Kardex)
class AdminKardex(admin.ModelAdmin):
    list_display = Attr(Kardex)
    list_display_links = Attr(Kardex)
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'style': 'width:80%'})
        },
        models.TextField: {
            'widget': Textarea(attrs={'style': 'width:80%'})
        },
    }


@admin.register(ImagenesProducto)
class AdminImagenesProducto(admin.ModelAdmin):
    list_display = Attr(ImagenesProducto)
    list_display_links = Attr(ImagenesProducto)


@admin.register(DireccionProveedor)
class AdminDireccion(admin.ModelAdmin):
    list_display = Attr(DireccionProveedor)
    list_display_links = Attr(DireccionProveedor)
