from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento
from Producto.models import Productos


def proformas(request,id=0):
    establecimiento=None
    establecimientos=None
    productos=None
    if int(id) > 0:
        establecimiento = Establecimiento.objects.get(id=id)
        productos = Productos.objects.filter(establecimiento_id=id)
        print(productos)
    else:
        establecimientos = Establecimiento.objects.filter(usuario=request.user)

    contexto={
        'establecimiento':establecimiento,
        'establecimientos':establecimientos,
        'productos':productos,
    }
    return render(request, 'Ventas/proformas.html', contexto)