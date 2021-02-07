from django import template
from django.db.models import Sum

from Producto.models import Productos, Kardex, Precios
from Ventas.models import Recibos, CuentasCobrar

register = template.Library()

@register.simple_tag
def pagos(id_cuenta):
    xpagos=0
    try:
        xpagos=Recibos.objects.filter(cuenta_id=id_cuenta).aggregate(Sum('cantidad'))['cantidad__sum']
        if xpagos == None:
            xpagos=0
    except:
        xpagos =0
    return round(xpagos,2)

@register.simple_tag
def saldos(id_cuenta):
    cuenta=CuentasCobrar.objects.get(id=id_cuenta).cantidad
    xpagos=0
    try:
        xpagos=Recibos.objects.filter(cuenta_id=id_cuenta).aggregate(Sum('cantidad'))['cantidad__sum']
        if xpagos==None:
            xpagos=0
    except:
        xpagos =0

    print(cuenta,xpagos)
    total=cuenta - xpagos
    return round(total,2)