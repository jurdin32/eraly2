from django.contrib import admin

# Register your models here.
from Producto.models import Proveedor, DireccionProveedor
from eraly2.snippers import Attr

class DireccionInline(admin.StackedInline):
    model = DireccionProveedor
    extra = 0

@admin.register(Proveedor)
class AdminProveedor(admin.ModelAdmin):
    list_display = Attr(Proveedor)
    list_display_links = Attr(Proveedor)
    inlines = [DireccionInline]


@admin.register(DireccionProveedor)
class AdminDireccion(admin.ModelAdmin):
    list_display = Attr(DireccionProveedor)
    list_display_links = Attr(DireccionProveedor)
