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
    except:
        xpagos =0
    return xpagos

@register.simple_tag
def saldos(id_cuenta):
    cuenta=CuentasCobrar.objects.get(id=id_cuenta).cantidad
    xpagos=0
    try:
        xpagos=Recibos.objects.filter(cuenta_id=id_cuenta).aggregate(Sum('cantidad'))['cantidad__sum']
    except:
        xpagos =0
    return float(str(cuenta)) - float(str(xpagos))