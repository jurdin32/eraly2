from django.contrib import admin

# Register your models here.
from Ventas.models import *
from eraly2.snippers import Attr

@admin.register(Facturas)
class AdminFacturas(admin.ModelAdmin):
    list_display = Attr(Facturas)
    list_display_links = Attr(Facturas)

@admin.register(DetalleFactura)
class AdminFacturas(admin.ModelAdmin):
    list_display = Attr(DetalleFactura)
    list_display_links = Attr(DetalleFactura)

@admin.register(CuentasCobrar)
class AdminCuentasCobrar(admin.ModelAdmin):
    list_display = Attr(CuentasCobrar)
    list_display_links = Attr(CuentasCobrar)

@admin.register(Recibos)
class AdminRecibos(admin.ModelAdmin):
    list_display = Attr(Recibos)
    list_display_links = Attr(Recibos)