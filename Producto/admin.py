from django.contrib import admin

# Register your models here.
from Producto.models import Proveedor
from eraly2.snippers import Attr


@admin.register(Proveedor)
class AdminProveedor(admin.ModelAdmin):
    list_display = Attr(Proveedor)
    list_display_links = Attr(Proveedor)
