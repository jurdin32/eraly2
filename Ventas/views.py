from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import ProcessFormView

from Empresa.models import Establecimiento, ConfigurarDocumentos
from Home.models import Provincia
from Personas.models import Clientes
from Producto.models import Productos, Kardex, Precios
from Ventas.models import Facturas, DetalleFactura, CuentasCobrar, Recibos
from eraly2.settings import BASE_DIR
from eraly2.snippers import render_pdf_view, export_pdf
from nlt import numlet as nl

def proformas(request,id=0):
    establecimiento=None
    establecimientos=None
    productos=None
    clientes=Clientes.objects.filter(establecimiento__usuario=request.user)
    proformaContador=""
    print(proformaContador)
    if int(id) > 0:
        establecimiento = Establecimiento.objects.get(id=id)
        productos = Productos.objects.filter(establecimiento_id=id)
        numero=ConfigurarDocumentos.objects.get(establecimiento=establecimiento)
        proformaContador=str(numero.proformas + Facturas.objects.filter(tipo="P",establecimiento=establecimiento).count()).zfill(10)

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
        'precios':Precios.objects.all(),
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
        numero=ConfigurarDocumentos.objects.get(establecimiento=establecimiento)
        proformaContador=str(numero.facturas+Facturas.objects.filter(tipo="F", establecimiento=establecimiento).count()).zfill(10)

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
        'precios': Precios.objects.all(),
    }
    return render(request, 'Ventas/facturas.html', contexto)

def eliminarregistrosFacturaProforma(id):
    try:
        detalles = DetalleFactura.objects.filter(factura_id=id)
        detalles.delete()
    except:
        pass

def registrarDocumento(request,id):
    factura=None
    if request.POST:
        print(request.POST)
        try:
            factura= Facturas.objects.get(id = request.POST["tipo"])
            factura.establecimiento_id=request.POST['establecimiento']
            factura.cliente_id=request.POST["cliente"]
            factura.subtotal=request.POST["subtotal"]
            factura.iva=request.POST["iva"]
            factura.total=request.POST["total"]
            factura.save()
            for detalle in DetalleFactura.objects.filter(factura=factura):
                Kardex(producto=detalle.producto, tipo="I", cantidad=detalle.cantidad,
                       descripcion="Registrado segun modificación de factura de compra No. %s, Reposicion por devolucion de productos." % (
                           factura.numero)).save()
            eliminarregistrosFacturaProforma(factura.id)
            return HttpResponse(factura.id)
        except:
            documento = Facturas.objects.create(establecimiento_id=request.POST['establecimiento'],
                                                cliente_id=request.POST["cliente"],tipo=request.POST["tipo"],
                                                numero=request.POST["numero"],
                 subtotal=request.POST["subtotal"],iva=request.POST["iva"],total=request.POST["total"])
            documento.save()

            print(documento)
            return HttpResponse(documento.id)
        return HttpResponse(0)



def registrarDetallesFacturaProforma(request,id):
    if request.POST:
        DetalleFactura(factura_id=request.POST['factura_id'],producto_id=request.POST['producto_id'],precioU=request.POST['precio'],cantidad=request.POST['cantidad'],
                       subtotal=request.POST['subtotal']).save()
        return HttpResponse("ok")

def registroClienteFacturaProforma(request,id):
    if request.POST:
        print(request.POST)
        Clientes(establecimiento_id=id, cedula=request.POST['cedula'], nombres=request.POST['nombres'],
                 apellidos=request.POST['apellidos'],ciudad_id=request.POST['ciudad'],
                 direccion=request.POST['direccion'],
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
        'items': (10 - detalles.count()) * "*",
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
    documentos =None
    if int(request.GET["establecimiento"])==0:
        documentos = Facturas.objects.filter(establecimiento__usuario=request.user)
    else:
        documentos=Facturas.objects.filter(establecimiento_id=request.GET["establecimiento"])

    contexto={
        'documentos':documentos,
        "establecimientos":Establecimiento.objects.filter(usuario=request.user),
    }
    return render(request, 'Ventas/ListaDocumentos.html',contexto)


def editarDocumentos(request,id):
    documento=Facturas.objects.get(id=id)
    contexto={
        'documento':documento,
        'detalles':DetalleFactura.objects.filter(factura=documento),
        'establecimiento':documento.establecimiento,
        'productos':Productos.objects.filter(establecimiento=documento.establecimiento),
        'clientes':Clientes.objects.filter(establecimiento=documento.establecimiento),
        'precios':Precios.objects.filter(producto__establecimiento__usuario=request.user),
    }
    return render(request, 'Ventas/editDocumentos.html', contexto)

def anularDocumento(request,id):
    documento= Facturas.objects.get(id=id)
    if documento.estado=="E":
        documento.estado="A"
        for detalle in DetalleFactura.objects.filter(factura=documento):
            Kardex(producto=detalle.producto, tipo="I", cantidad=detalle.cantidad,
                   descripcion="Registrado segun anulación de factura de compra No. %s, Reposicion por devolucion de productos." % (
                       documento.numero)).save()
        messages.add_message(request, messages.INFO, "El Documento se ha anulado.!")
        documento.save()

    else:
        messages.add_message(request, messages.ERROR, "No es posible deshabilitar una factura varias veces.!")
    return HttpResponseRedirect('/document/list/')

def cuentasCobrar(request):
    if request.POST:
        CuentasCobrar(cantidad=request.POST['cantidad'], cliente_id=request.POST['cliente'],factura_numero=request.POST['factura_numero']).save()
        messages.add_message(request, messages.SUCCESS, "El Documento se ha registrado.!")
    contexto={
        'cuentas':CuentasCobrar.objects.filter(cliente__establecimiento__usuario=request.user),
        'clientes':Clientes.objects.filter(establecimiento__usuario=request.user)
    }
    return render(request, 'Ventas/ListaCuentasCobrar.html',contexto)

def abonos(request,id):
    if request.POST:
        Recibos(cuenta_id=id,cantidad=request.POST['cantidad'],formaPago=request.POST['formaPago'],numeroCheque=request.POST['cheque'],rebidoPor=request.user, recibiDe=request.POST['recibidoDe']).save()
        messages.add_message(request, messages.SUCCESS, "El Documento se ha registrado.!")
    contexto={
        'abonos': Recibos.objects.filter(cuenta_id = id),
        'cuenta':CuentasCobrar.objects.get(id=id),
    }
    return render(request, 'Ventas/abonos.html', contexto)

def crearAbonosPDF(request, id):
    recibo=Recibos.objects.get(id=id)
    resultado = nl.Numero(recibo.cantidad).a_letras
    print(resultado)
    contexto={
        'recibo':recibo,
        'site': Site.objects.last(),
        'abono':resultado
    }
    return export_pdf(request,'Ventas/rptAbonos.html',contexto)