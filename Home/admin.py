from django.contrib import admin

# Register your models here.
from Home.models import Usuario, Direccion, Tienda
from eraly2.snippers import Attr


@admin.register(Usuario)
class AdminUsuario(admin.ModelAdmin):
    list_display = Attr(Usuario)
    list_display_links = Attr(Usuario)


@admin.register(Direccion)
class AdminDirecciones(admin.ModelAdmin):
    list_display = Attr(Direccion)
    list_display_links = Attr(Direccion)

@admin.register(Tienda)
class AdminTiendas(admin.ModelAdmin):
    list_display_links = Attr(Tienda)
    list_display = Attr(Tienda)