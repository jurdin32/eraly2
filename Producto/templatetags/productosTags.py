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