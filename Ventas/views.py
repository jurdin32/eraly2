from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import ProcessFormView

from Empresa.models import Establecimiento
from Home.models import Provincia
from Personas.models import Clientes
from Producto.models import Productos
from Ventas.models import Facturas


def proformas(request,id=0):
    establecimiento=None
    establecimientos=None
    productos=None
    clientes=None
    proformaContador=""
    print(proformaContador)
    if int(id) > 0:
        establecimiento = Establecimiento.objects.get(id=id)
        productos = Productos.objects.filter(establecimiento_id=id)
        clientes=Clientes.objects.filter(establecimiento_id=id)
        proformaContador=str(Facturas.objects.filter(tipo="P").count()+1).zfill(10)

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
        'clientes':clientes,
        'provincias':Provincia.objects.all(),
        'contadorProforma':proformaContador,
    }
    return render(request, 'Ventas/proformas.html', contexto)


def registrarDocumento(request,id):
    try:
        if request.POST:
            Facturas(establecimiento_id=request.POST['establecimiento'],cliente_id=request.POST["cliente"],tipo=request.POST["tipo"],numero=request.POST["numero"],
                 subtotal=request.POST["subtotal"],iva=request.POST["iva"],total=request.POST["total"]).save()
            return HttpResponse(1)
    except:
        return HttpResponse(0)

def registroClienteFacturaProforma(request,id):
    if request.POST:
        print(request.POST)
        Clientes(establecimiento_id=id, cedula=request.POST['cedula'], nombres=request.POST['nombres'],apellidos=request.POST['apellidos'],ciudad_id=request.POST['ciudad'],
                 telefono=request.POST['telefono'],celular=request.POST['celular']).save()
        messages.add_message(request, messages.SUCCESS, "El registro se Creado..!")
    return HttpResponseRedirect("/proforms/%s/"%id)