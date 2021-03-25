from django import template
from django.db.models import Sum, Avg
import datetime

from Producto.models import *

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

@register.simple_tag
def rating_productos(id):
    rating=CalificacionProductos.objects.filter(producto_id=id).aggregate(rating=Avg('rating'))
    if rating['rating']==None :
        return 0
    return round(float(rating['rating']))

@register.simple_tag
def contador_producto(id):
    rating=CalificacionProductos.objects.filter(producto_id=id).count()
    return rating

@register.simple_tag
def promocion_descuento(id):
    promo=Promociones.objects.filter(precio__producto_id=id).last()
    fecha=datetime.datetime.now().date()
    if promo:
        if fecha >= promo.fechaInicio and fecha <= promo.fechaFinal:
         return mark_safe("""<div class="product-label">
                    <span class="discount">
                        %s
                    </span>
                </div>"""%promo.descuento)
    return ""

@register.simple_tag
def promocion_precio(id):
    promo=Promociones.objects.filter(precio__producto_id=id).last()
    fecha=datetime.datetime.now().date()
    if promo:
        if fecha >= promo.fechaInicio and fecha <= promo.fechaFinal:
            return promo.total
    return 0