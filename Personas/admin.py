from django.contrib import admin
from Personas.models import *
from eraly2.snippers import Attr


@admin.register(Clientes)
class AdminTipoProveedor(admin.ModelAdmin):
    list_display = Attr(Clientes)
    list_display_links = Attr(Clientes)

@admin.register(UsuariosWeb)
class AdminUsuarioWeb(admin.ModelAdmin):
    list_display = Attr(UsuariosWeb)
    list_display_links = Attr(UsuariosWeb)

@admin.register(DireccionesWeb)
class AdminDireccionesWeb(admin.ModelAdmin):
    list_display = Attr(DireccionesWeb)
    list_display_links = Attr(DireccionesWeb)