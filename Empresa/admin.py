from django.contrib import admin

# Register your models here.
from Empresa.models import Direccion, Establecimiento
from eraly2.snippers import Attr


class DireccionInline(admin.StackedInline):
    extra = 0
    model = Direccion

@admin.register(Direccion)
class AdminDirecciones(admin.ModelAdmin):
    list_display = Attr(Direccion)
    list_display_links = Attr(Direccion)

@admin.register(Establecimiento)
class AdminTiendas(admin.ModelAdmin):
    list_display_links = Attr(Establecimiento)
    list_display = Attr(Establecimiento)
    inlines = [DireccionInline]