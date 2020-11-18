from django.contrib import admin

# Register your models here.
from Home.models import Usuario, Direccion, Tienda, Pais, Provincia, Ciudad
from eraly2.snippers import Attr


@admin.register(Usuario)
class AdminUsuario(admin.ModelAdmin):
    list_display = Attr(Usuario)
    list_display_links = Attr(Usuario)

class DireccionInline(admin.StackedInline):
    extra = 0
    model = Direccion

@admin.register(Direccion)
class AdminDirecciones(admin.ModelAdmin):
    list_display = Attr(Direccion)
    list_display_links = Attr(Direccion)

@admin.register(Tienda)
class AdminTiendas(admin.ModelAdmin):
    list_display_links = Attr(Tienda)
    list_display = Attr(Tienda)
    inlines = [DireccionInline]

class ProvinciaInline(admin.StackedInline):
    model = Provincia
    extra = 0

@admin.register(Pais)
class AdminPais(admin.ModelAdmin):
    list_display_links = Attr(Pais)
    list_display = Attr(Pais)
    inlines = [ProvinciaInline]

class CiudadInline(admin.StackedInline):
    model = Ciudad
    extra = 0

@admin.register(Provincia)
class AdminProvincia(admin.ModelAdmin):
    list_display_links = Attr(Provincia)
    list_display = Attr(Provincia)
    inlines = [CiudadInline]

@admin.register(Ciudad)
class AdminCiudad(admin.ModelAdmin):
    list_display_links = Attr(Ciudad)
    list_display = Attr(Ciudad)