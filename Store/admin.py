from django.contrib import admin

# Register your models here.
from Store.models import Publicidad, ComprasWeb, DetalleCompraWeb, Favoritos
from eraly2.snippers import Attr


@admin.register(Publicidad)
class AdminPublicidad(admin.ModelAdmin):
    list_display = Attr(Publicidad)
    list_display_links = Attr(Publicidad)

@admin.register(ComprasWeb)
class AdminComprasWeb(admin.ModelAdmin):
    list_display = Attr(ComprasWeb)
    list_display_links = Attr(ComprasWeb)

@admin.register(DetalleCompraWeb)
class AdminDetalleCompraWeb(admin.ModelAdmin):
    list_display = Attr(DetalleCompraWeb)
    list_display_links = Attr(DetalleCompraWeb)

@admin.register(Favoritos)
class AdminFavorito(admin.ModelAdmin):
    list_display = Attr(Favoritos)
    list_display_links = Attr(Favoritos)