from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento


def proformas(request,id=0):
    establecimiento=None
    establecimientos=None
    if int(id) > 0:
        establecimiento = Establecimiento.objects.get(id=id)
    else:
        establecimientos = Establecimiento.objects.filter(usuario=request.user)

    contexto={
        'establecimiento':establecimiento,
        'establecimientos':establecimientos
    }
    return render(request, 'Ventas/proformas.html', contexto)