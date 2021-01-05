from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from Empresa.models import Establecimiento
from Personas.models import Clientes
from Producto.models import Productos


def proformas(request,id=0):
    establecimiento=None
    establecimientos=None
    productos=None
    clientes=None

    if int(id) > 0:
        establecimiento = Establecimiento.objects.get(id=id)
        productos = Productos.objects.filter(establecimiento_id=id)
        clientes=Clientes.objects.filter(establecimiento_id=id)
    else:
        establecimientos = Establecimiento.objects.filter(usuario=request.user)
        contador=establecimientos.count()
        if contador == 1:
            for esta in establecimientos:
                return HttpResponseRedirect("/proforms/%s/"%esta.id)
    contexto={
        'establecimiento':establecimiento,
        'establecimientos':establecimientos,
        'productos':productos,
        'clientes':clientes
    }
    return render(request, 'Ventas/proformas.html', contexto)