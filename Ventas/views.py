from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import ProcessFormView

from Empresa.models import Establecimiento
from Home.models import Provincia
from Personas.models import Clientes
from Producto.models import Productos
from Ventas.models import Facturas, DetalleFactura
from eraly2.settings import BASE_DIR
from eraly2.snippers import render_pdf_view, export_pdf


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

def facturas(request,id=0):
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
        proformaContador=str(Facturas.objects.filter(tipo="F").count()+1).zfill(10)

    else:
        establecimientos = Establecimiento.objects.filter(usuario=request.user)
        contador=establecimientos.count()
        if contador == 1:
            for esta in establecimientos:
                return HttpResponseRedirect("/billing/%s/"%esta.id)
    contexto={
        'establecimiento':establecimiento,
        'establecimientos':establecimientos,
        'productos':productos,
        'clientes':clientes,
        'provincias':Provincia.objects.all(),
        'contadorProforma':proformaContador,
    }
    return render(request, 'Ventas/facturas.html', contexto)


def registrarDocumento(request,id):
    try:
        if request.POST:
            documento = Facturas.objects.create(establecimiento_id=request.POST['establecimiento'],cliente_id=request.POST["cliente"],tipo=request.POST["tipo"],numero=request.POST["numero"],
                 subtotal=request.POST["subtotal"],iva=request.POST["iva"],total=request.POST["total"])
            documento.save()

            print(documento)
            return HttpResponse(documento.id)
    except:
        return HttpResponse(0)

def registrarDetallesFacturaProforma(request,id):
    if request.POST:
        DetalleFactura(factura_id=request.POST['factura_id'],producto_id=request.POST['producto_id'],precioU=request.POST['precio'],cantidad=request.POST['cantidad'],
                       subtotal=request.POST['subtotal']).save()
        return HttpResponse("ok")

def registroClienteFacturaProforma(request,id):
    if request.POST:
        print(request.POST)
        Clientes(establecimiento_id=id, cedula=request.POST['cedula'], nombres=request.POST['nombres'],apellidos=request.POST['apellidos'],ciudad_id=request.POST['ciudad'],
                 telefono=request.POST['telefono'],celular=request.POST['celular']).save()
        messages.add_message(request, messages.SUCCESS, "El registro se Creado..!")
    return HttpResponseRedirect("/proforms/%s/"%id)

def crearDocumentoPDF_Proforma(request, id):
    documento=Facturas.objects.get(id=id)
    detalles=DetalleFactura.objects.filter(factura_id=id)
    contexto={
        'documento':documento,
        'detalles':detalles,
        'site': Site.objects.last(),
        'items': (12 - detalles.count()) * "*",
    }
    return export_pdf(request,'Ventas/rptProforma.html',contexto)
    #return render(request, 'Ventas/rptProforma.html', contexto)

def crearDocumentoPDF_Factura(request, id):
    detalles=DetalleFactura.objects.filter(factura_id=id)
    contexto={
        'documento':Facturas.objects.get(id=id),
        'detalles':detalles,
        'items':(10 - detalles.count())*"*",
        'site':Site.objects.last(),
    }
    print((10 - detalles.count()))
    return render_pdf_view(request,'Ventas/rptFactura.html',contexto)
    #return render(request,'Ventas/rptFactura.html',contexto)

def listaDocumentos(request):
    contexto={
        'documentos':Facturas.objects.filter(establecimiento__usuario=request.user)
    }
    return render(request, 'Ventas/ListaDocumentos.html',contexto)
