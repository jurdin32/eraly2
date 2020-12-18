from django.shortcuts import render
# Create your views here.
from Empresa.models import Establecimiento
from Producto.models import Proveedor, ActividadProveedor, TipoProveedor


def proveedores(request):
    mensaje=""
    tipo=""
    if request.POST:
        try:
            if request.FILES:
                Proveedor.objects.create(establecimiento_id=request.POST['establecimiento'],logo=request.FILES['logo'], ruc=request.POST['ruc'],nombre_fantasia=request.POST['nombreComercial'],
                                         representante=request.POST['representateLegal']).save()
            else:
                Proveedor.objects.create(establecimiento_id=request.POST['establecimiento'],
                                         ruc=request.POST['ruc'], nombre_fantasia=request.POST['nombreComercial'],
                                         representante=request.POST['representateLegal']).save()
            mensaje = "El registro se ha creado exitosamente..! "
            tipo = "success"
        except Exception as error:
            mensaje="Al parecer ocurrio un error: "+str(error)
            tipo="danger"
    contexto={
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'proveedores': Proveedor.objects.filter(establecimiento__usuario=request.user),
        'mensaje':mensaje,
        'tipo':tipo,

    }
    return render(request, "producto/proveedores.html",contexto)

def editarProveedor(request,id):
    mensaje = ""
    tipo = ""
    proveedor=Proveedor.objects.get(id=id)
    if request.POST:
        print(request.POST)
        proveedor.establecimiento_id=request.POST['establecimiento']
        proveedor.ruc=request.POST['ruc']
        proveedor.nombre_fantasia=request.POST['nombreComercial']
        proveedor.representante=request.POST['representateLegal']
        if request.FILES:
            proveedor.logo=request.FILES['logo']
        proveedor.save()
        mensaje="El registro se ha Modificado exitosamente..!"
        tipo='success'
    contexto={
        "proveedor":proveedor,
        'establecimientos':Establecimiento.objects.filter(usuario=request.user),
        'mensaje':mensaje,
        'tipo':tipo
    }
    return render(request, "producto/editarProveedores.html",contexto)

def actividadesProveedor(request,id):
    mensaje = ""
    tipo = ""
    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        print(request.POST)
        ActividadProveedor.objects.create(proveedor_id=id,nombre=request.POST['nombreActividad'],detalle=request.POST['detalleActividad']).save()
        mensaje = "Se ha creado nueva actividad para el proveedor..!"
        tipo = 'success'
    contexto={
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'mensaje': mensaje,
        'tipo': tipo
    }
    return render(request, "producto/editarProveedores.html",contexto)

def eliminarActividades(request,id):
    mensaje = ""
    tipo = ""
    actividad=ActividadProveedor.objects.get(id=id)
    proveedor = actividad.proveedor
    actividad.delete()
    mensaje = "El registro se ha borrado..!"
    tipo = 'success'
    contexto = {
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'mensaje': mensaje,
        'tipo': tipo
    }
    return render(request, "producto/editarProveedores.html", contexto)

def tipoProveedor(request,id):
    mensaje = ""
    tipo = ""
    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        TipoProveedor.objects.create(proveedor_id=id,detalle=request.POST['detalle']).save()
        mensaje = "El registro se ha registrado el nuevo tipo..!"
        tipo = 'success'
    contexto = {
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'mensaje': mensaje,
        'tipo': tipo
    }
    return render(request, "producto/editarProveedores.html", contexto)

def eliminartipoProveedor(request,id):
    mensaje = ""
    tipo = ""
    tp=TipoProveedor.objects.get(id=id)
    proveedor=tp.proveedor
    tp.delete()
    mensaje = "El registro se ha eliminado el  tipo..!"
    tipo = 'success'
    contexto = {
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'mensaje': mensaje,
        'tipo': tipo
    }
    return render(request, "producto/editarProveedores.html", contexto)

def productos(request):
    contexto={

    }
    return render(request, "producto/productos.html",contexto)

def categorias(request):
    contexto={

    }
    return render(request, "producto/categorias.html",contexto)

def kardex(request):
    contexto={

    }
    return render(request, "producto/kardex.html",contexto)