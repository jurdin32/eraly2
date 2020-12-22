from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from Empresa.models import Establecimiento
from Home.models import Provincia
from Producto.models import Proveedor, ActividadProveedor, TipoProveedor, DireccionProveedor, Categorias, Subcategorias
from django.contrib import messages

from eraly2.settings import BASE_DIR


def proveedores(request):
    if request.POST:
        try:
            if request.FILES:
                Proveedor.objects.create(establecimiento_id=request.POST['establecimiento'],logo=request.FILES['logo'], ruc=request.POST['ruc'],nombre_fantasia=request.POST['nombreComercial'],
                                         representante=request.POST['representateLegal']).save()
            else:
                Proveedor.objects.create(establecimiento_id=request.POST['establecimiento'],
                                         ruc=request.POST['ruc'], nombre_fantasia=request.POST['nombreComercial'],
                                         representante=request.POST['representateLegal']).save()
            messages.add_message(request, messages.SUCCESS, "El registro se ha creado éxitosamente..!")
        except:
            messages.add_message(request, messages.ERROR, "Al parecer ocurrio un error..!")
    contexto={
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'proveedores': Proveedor.objects.filter(establecimiento__usuario=request.user),
        'provincias': Provincia.objects.all(),
    }
    return render(request, "producto/proveedores.html",contexto)

def editarProveedor(request,id):
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
        messages.add_message(request, messages.INFO, "El registro se ha modificado éxitosamente..!")
    contexto={
        "proveedor":proveedor,
        'establecimientos':Establecimiento.objects.filter(usuario=request.user),
        'provincias': Provincia.objects.all(),
    }
    return render(request, "producto/editarProveedores.html",contexto)

def eliminarProveedor(request,id):
    proveedor=Proveedor.objects.get(id=id)
    proveedor.delete()
    messages.add_message(request, messages.WARNING, "El Proveedor se ha eliminado..!")
    return HttpResponseRedirect('/suppliers/')


def actividadesProveedor(request,id):

    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        print(request.POST)
        ActividadProveedor.objects.create(proveedor_id=id,nombre=request.POST['nombreActividad'],detalle=request.POST['detalleActividad']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado Nueva actividad del Proveedor..!")
    contexto={
        "proveedor": proveedor,
        'provincias': Provincia.objects.all(),
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
    }
    return render(request, "producto/editarProveedores.html",contexto)

def eliminarActividades(request,id):
    actividad=ActividadProveedor.objects.get(id=id)
    proveedor = actividad.proveedor.id
    actividad.delete()
    messages.add_message(request, messages.WARNING, "El registro se ha eliminado..!")
    return HttpResponseRedirect('/suppliers/edit/%s/' % proveedor)

def tipoProveedor(request,id):
    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        TipoProveedor.objects.create(proveedor_id=id,detalle=request.POST['detalle']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado el nuevo tipo..!")
    contexto = {
        'provincias': Provincia.objects.all(),
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
    }
    return render(request, "producto/editarProveedores.html", contexto)

def eliminartipoProveedor(request,id):
    tp=TipoProveedor.objects.get(id=id)
    proveedor=tp.proveedor.id
    tp.delete()
    messages.add_message(request,messages.WARNING,"El registro se ha eliminado..!")
    return HttpResponseRedirect('/suppliers/edit/%s/' % proveedor)

def direccionProveedor(request,id):
    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        DireccionProveedor.objects.create(proveedor_id=id,ciudad_id=request.POST['ciudad'],direccion=request.POST["direccion"],telefono=request.POST['telefono']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado la nueva dirección..!")
    contexto = {
        'provincias': Provincia.objects.all(),
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
    }
    return render(request, "producto/editarProveedores.html", contexto)

def eliminarDireccionProveedores(request,id):
    tp=DireccionProveedor.objects.get(id=id)
    proveedor=tp.proveedor.id
    tp.delete()
    messages.add_message(request,messages.WARNING,"El registro se ha eliminado..!")
    return HttpResponseRedirect('/suppliers/edit/%s/'%proveedor)

def productos(request):
    contexto={

    }
    return render(request, "producto/productos.html",contexto)


def iconos_text():
    iconos=[]
    for icono in open(str(BASE_DIR)+"/static/iconos.txt",'r').readlines():
        icono=icono.strip().replace("(alias)","")
        iconos.append(icono)
    return iconos

def categorias(request):
    if request.POST:
        Categorias.objects.create(establecimiento_id=request.POST['establecimiento'], icono="fa "+request.POST["icono"],
                                  nombre=request.POST["nombre"], descripcion=request.POST['detalle']).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    contexto={
        'categorias':Categorias.objects.filter(establecimiento__usuario=request.user),
        'iconos':iconos_text(),
        'establecimientos':Establecimiento.objects.filter(usuario=request.user)
    }
    return render(request, "producto/categorias.html",contexto)

def editarCategoria(request,id):
    if request.POST:
        print(request.POST)
        categoria=Categorias.objects.get(id=id)
        categoria.establecimiento_id=request.POST['establecimiento']
        categoria.icono="fa "+request.POST["icono"]
        categoria.nombre=request.POST["nombre"]
        categoria.descripcion=request.POST['detalle']
        categoria.save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha actualizado..!")
    return  HttpResponseRedirect('/category/')

def eliminarCategoria(request,id):
    cat = Categorias.objects.get(id=id)
    cat.delete()
    messages.add_message(request, messages.WARNING, "El registro se ha eliminado..!")
    return HttpResponseRedirect('/category/')


def subcategorias(request,id):
    if request.POST:
        Subcategorias.objects.create(categoria_id=id, icono="fa "+request.POST["icono"],nombre=request.POST["nombre"],
                                     descripcion=request.POST['detalle']).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    contexto={
        'categoria':Categorias.objects.get(id=id),
        'subcategorias':Subcategorias.objects.filter(categoria_id=id),
        'iconos': iconos_text(),
    }
    return render(request, "producto/subcategorias.html",contexto)

def editarSubCategoria(request,id):
    categoria = Subcategorias.objects.get(id=id)
    if request.POST:
        print(request.POST)
        categoria.icono="fa "+request.POST["icono"]
        categoria.nombre=request.POST["nombre"]
        categoria.descripcion=request.POST['detalle']
        categoria.save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha actualizado..!")
    return  HttpResponseRedirect('/category/%s'%categoria.categoria_id)

def eliminarSubcategoria(request,id):
    sub = Subcategorias.objects.get(id=id)
    cat = sub.categoria.id
    sub.delete()
    messages.add_message(request, messages.WARNING, "El registro se ha eliminado..!")
    return HttpResponseRedirect('/category/%s' % cat)


def kardex(request):
    contexto={

    }
    return render(request, "producto/kardex.html",contexto)