from django import template
from django.db.models import Sum

from Producto.models import Productos, Kardex

register = template.Library()

@register.simple_tag
def stock(id):
    kardex=Kardex.objects.filter(producto_id=id)
    ingresos=kardex.filter(tipo="I").aggregate(Sum('cantidad'))['cantidad__sum']
    egresos=kardex.filter(tipo="E").aggregate(Sum('cantidad'))['cantidad__sum']
    if ingresos==None:
        ingresos=0
    if egresos==None:
        egresos=0
    return ingresos-egresos

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