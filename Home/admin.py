from django.contrib import admin

# Register your models here.
from Home.models import Pais, Provincia, Ciudad, ConfigurarDocumentos
from eraly2.snippers import Attr


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

@admin.register(ConfigurarDocumentos)
class AdminConfigurarDocumentos(admin.ModelAdmin):
    list_display = Attr(ConfigurarDocumentos)
    list_display_links = Attr(ConfigurarDocumentos)