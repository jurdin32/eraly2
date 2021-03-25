from django.contrib import admin

# Register your models here.
from Store.models import Publicidad
from eraly2.snippers import Attr


@admin.register(Publicidad)
class AdminPublicidad(admin.ModelAdmin):
    list_display = Attr(Publicidad)
    list_display_links = Attr(Publicidad)