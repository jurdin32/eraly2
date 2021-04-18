from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from Empresa.models import Establecimiento, ConfigurarDocumentos
from Home.models import Provincia
from Personas.models import Clientes
from Producto.models import Productos, Kardex, Precios
from Store.models import DetalleCompraWeb, ComprasWeb
from Ventas.models import Facturas, DetalleFactura, CuentasCobrar, Recibos
from eraly2.snippers import export_pdf
from nlt import numlet as nl

def proformas(request,id=0):
    establecimiento=None
    establecimientos=None
    productos=None
    clientes=Clientes.objects.filter(establecimiento__usuarioempresa__user=request.user)
    contadorDocumentos=""
    tipo=request.GET.get('tipo')

    if int(id) > 0:
        establecimiento = Establecimiento.objects.get(id=id)
        productos = Productos.objects.filter(establecimiento_id=id)
        numero=ConfigurarDocumentos.objects.get(establecimiento=establecimiento)
        if tipo=="P":
            contadorDocumentos=str(numero.proformas + Facturas.objects.filter(tipo=tipo,establecimiento=establecimiento).count()).zfill(10)
        else:
            contadorDocumentos = str(numero.facturas + Facturas.objects.filter(tipo=tipo, establecimiento=establecimiento).count()).zfill(10)

    else:
        establecimientos = Establecimiento.objects.filter(usuarioempresa__user=request.user)
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
        'contadorProforma':contadorDocumentos,
        'precios':Precios.objects.all(),
        'tipo':tipo,
    }
    return render(request, 'Ventas/proformas.html', contexto)


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
            if factura.tipo=="F":
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
        Clientes(establecimiento_id=id, cedula=request.POST['cedula'], nombres=request.POST['nombres'], email=request.POST['email'],
                 apellidos=request.POST['apellidos'],ciudad_id=request.POST['ciudad'],
                 direccion=request.POST['direccion'],
                 telefono=request.POST['telefono'],celular=request.POST['celular']).save()
        messages.add_message(request, messages.SUCCESS, "El registro se Creado..!")
    if request.GET.get('tipo'):
        return HttpResponseRedirect("/proforms/%s/?tipo=%s"%(id,request.GET.get('tipo')))
    else:
        return HttpResponseRedirect("/clients/0/")

def crearDocumentoPDF_Proforma(request, id):
    documento=Facturas.objects.get(id=id)
    detalles=DetalleFactura.objects.filter(factura_id=id)
    contexto={
        'documento':documento,
        'detalles':detalles,

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
    }
    print((10 - detalles.count()))
    return export_pdf(request,'Ventas/rptFactura.html',contexto)
    #return render(request,'Ventas/rptFactura.html',contexto)

def listaDocumentos(request):
    documentos =None
    if int(request.GET["establecimiento"])==0:
        documentos = Facturas.objects.filter(establecimiento__usuarioempresa__user=request.user)
    else:
        documentos=Facturas.objects.filter(establecimiento_id=request.GET["establecimiento"])

    contexto={
        'documentos':documentos,
        "establecimientos":Establecimiento.objects.filter(usuarioempresa__user=request.user),
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
        'precios':Precios.objects.filter(producto__establecimiento__usuarioempresa__user=request.user),
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
        'cuentas':CuentasCobrar.objects.filter(cliente__establecimiento__usuarioempresa__user=request.user),
        'clientes':Clientes.objects.filter(establecimiento__usuarioempresa__user=request.user)
    }
    return render(request, 'Ventas/ListaCuentasCobrar.html',contexto)

def abonos(request,id):
    if request.POST:
        Recibos(cuenta_id=id,cantidad=request.POST['cantidad'],formaPago=request.POST['formaPago'],
                numeroCheque=request.POST['cheque'],rebidoPor=request.user, recibiDe=request.POST['recibidoDe']).save()
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
        'abono':resultado
    }
    return export_pdf(request,'Ventas/rptAbonos.html',contexto)

def autorizar_ComprasWeb(request):
    compras=DetalleCompraWeb.objects.filter(producto__establecimiento__usuarioempresa__user=request.user)
    contador=compras.count()

    if request.GET.get('establecimiento'):
        compras = compras.filter(producto__establecimiento_id=request.GET.get('establecimiento'))

    if request.POST:
        compra=compras.get(id=request.POST.get('producto_id'))
        compra.autorizado=True
        compra.save()
        messages.add_message(request,messages.SUCCESS,"Se ha autorizado el envío de mercaderías..!")
        return HttpResponseRedirect('/store/autority/?establecimiento=%s' %compra.producto.establecimiento_id)
    contexto={
        'comprasweb':compras,
        'total_compras':contador
    }
    return render(request,'Ventas/Ventas_Web.html',contexto)

def info_cliente_compra(request,hash):
    contexto={
        'compra':ComprasWeb.objects.get(hash=hash)
    }
    return render(request,'',contexto)