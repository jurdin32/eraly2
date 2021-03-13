import admin_thumbnails
from django.contrib import admin

# Register your models here.
from Empresa.models import *
from eraly2.snippers import Attr


class DireccionInline(admin.StackedInline):
    extra = 0
    model = Direccion

@admin.register(Direccion)
class AdminDirecciones(admin.ModelAdmin):
    list_display = Attr(Direccion)
    list_display_links = Attr(Direccion)

@admin.register(Establecimiento)
@admin_thumbnails.thumbnail('logo')
class AdminTiendas(admin.ModelAdmin):
    list_display_links = Attr(Establecimiento)
    list_display = ["previa"]+Attr(Establecimiento)
    inlines = [DireccionInline]

@admin.register(UsuarioEmpresa)
class AdminUsuario(admin.ModelAdmin):
    list_display = Attr(UsuarioEmpresa)
    list_display_links = Attr(UsuarioEmpresa)

@admin.register(ConfigurarDocumentos)
class AdminConfigurarDocumentos(admin.ModelAdmin):
    list_display = Attr(ConfigurarDocumentos)
    list_display_links = Attr(ConfigurarDocumentos)