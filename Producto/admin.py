from django.contrib import admin

# Register your models here.
from Producto.models import Proveedor, DireccionProveedor
from eraly2.snippers import Attr

class ProveedorInline(admin.StackedInline):
    model = Proveedor
    extra = 0

@admin.register(Proveedor)
class AdminProveedor(admin.ModelAdmin):
    list_display = Attr(Proveedor)
    list_display_links = Attr(Proveedor)


@admin.register(DireccionProveedor)
class AdminDireccion(admin.ModelAdmin):
    list_display = Attr(DireccionProveedor)
    list_display_links = Attr(DireccionProveedor)
    inlines = [ProveedorInline]