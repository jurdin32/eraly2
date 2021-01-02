from django.contrib import admin
from Personas.models import Clientes
from eraly2.snippers import Attr


@admin.register(Clientes)
class AdminTipoProveedor(admin.ModelAdmin):
    list_display = Attr(Clientes)
    list_display_links = Attr(Clientes)
