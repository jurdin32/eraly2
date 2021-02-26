from django import template
from django.db.models import Sum
from django.utils.safestring import mark_safe

from Producto.models import Productos, Kardex, Precios

register = template.Library()

@register.simple_tag
def precioProducto(id):
    try:
        precio=Precios.objects.get(producto_id=id, estado=True)
        return precio.precioVenta
    except Exception as e:
        print(e)
        return 0.00

@register.simple_tag
def stock(id):
    try:
        kardex=Kardex.objects.filter(producto_id=id)
        ingresos=kardex.filter(tipo="I").aggregate(Sum('cantidad'))['cantidad__sum']
        egresos=kardex.filter(tipo="E").aggregate(Sum('cantidad'))['cantidad__sum']
        if ingresos==None:
            ingresos=0
        if egresos==None:
            egresos=0
        return ingresos-egresos
    except:
        pass

@register.simple_tag
def ingresos(id):
    kardex=Kardex.objects.filter(producto_id=id)
    ingresos=kardex.filter(tipo="I").aggregate(Sum('cantidad'))['cantidad__sum']
    if ingresos==None:
        ingresos=0
    return ingresos

@register.simple_tag
def egresos(id):
    kardex=Kardex.objects.filter(producto_id=id)
    egresos=kardex.filter(tipo="E").aggregate(Sum('cantidad'))['cantidad__sum']
    if egresos==None:
        egresos=0
    return egresos

# para obtener los datos de la promocion segun el id =producto
@register.simple_tag
def promocion_inicio(id):
    try:
        return Promociones.objects.get(id=id).fecha_inicio
    except:
        return "No se ha creado"

@register.simple_tag
def promocion_finalizacion(id):
    try:
        return Promociones.objects.get(id=id).fecha_finalizacion
    except:
        return "No se ha creado"

@register.simple_tag
def promocion_estado(id):
    try:
        promo= Promociones.objects.get(producto_id=id).estado
        if promo:
            return mark_safe("<i style='font-size:20px' class='fa fa-check-square-o text-success'></i>")
        else:
            return mark_safe("<i style='font-size:20px'  class='fa fa-frown-o text-danger'></i>")
    except:
        return mark_safe("<i style='font-size:20px' class='fa fa-frown-o text-danger'></i>")