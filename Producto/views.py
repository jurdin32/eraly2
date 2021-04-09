import random

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from Home.models import Provincia
from Producto.models import *
from django.contrib import messages
from eraly2.settings import BASE_DIR
from eraly2.snippers import Hash_parse


def proveedores(request):
    prov=Proveedor.objects.filter(establecimiento__usuario=request.user)
    if request.GET.get("q"):
        prov = Proveedor.objects.filter(establecimiento_id=request.GET.get("q"))
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
        'proveedores': prov,
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

def iconos_text():
    iconos=[]
    for icono in open(str(BASE_DIR)+"/static/iconos.txt",'r').readlines():
        icono=icono.strip().replace("(alias)","")
        iconos.append(icono)
    return iconos

def categorias(request):
    cat = Categorias.objects.filter(establecimiento__usuario=request.user)
    if request.GET.get("cat"):
        cat=Categorias.objects.filter(establecimiento_id=request.GET.get('cat'))

    if request.POST:
        cats=Categorias.objects.create(establecimiento_id=request.POST['establecimiento'],
                                  nombre=request.POST["nombre"], descripcion=request.POST['detalle'])
        cats.save()
        cats.slug=cats.nombre[0:2]+str(cats.id)
        cats.save()

        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    contexto={
        'categorias':cat,
        'iconos':iconos_text(),
        'establecimientos':Establecimiento.objects.filter(usuario=request.user)
    }
    return render(request, "producto/categorias.html",contexto)

def editarCategoria(request,id):
    if request.POST:
        print(request.POST)
        categoria=Categorias.objects.get(id=id)
        categoria.establecimiento_id=request.POST['establecimiento']
        categoria.nombre=request.POST["nombre"]
        categoria.descripcion=request.POST['detalle']
        categoria.slug = categoria.nombre[0:2] + str(categoria.id)
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
        Subcategorias.objects.create(categoria_id=id,nombre=request.POST["nombre"],
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


#------------ Productos ----------_#
def productos(request):
    productos=Productos.objects.filter(establecimiento__usuario=request.user)
    if request.GET.get('empresa'):
        productos = Productos.objects.filter(establecimiento_id=request.GET.get('empresa'))

    contexto={
        "productos":productos,
        "empresas":Establecimiento.objects.filter(usuario=request.user)
    }
    return render(request, "producto/productos.html",contexto)

def registarProducto(request):
    producto = Productos()
    contexto = {
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'categorias': Categorias.objects.filter(establecimiento__usuario=request.user),
        'marcas': Marca.objects.all(),
        'subcategorias':Subcategorias.objects.all(),
    }
    if request.POST:
        producto.establecimiento_id=request.POST['establecimiento']
        producto.subcategoria_id=request.POST['categoria']
        producto.nombre = request.POST['nombre']
        producto.tipo=request.POST['tipo']
        if request.POST.get('marca'):
            producto.marca_id = request.POST['marca']
        else:
            producto.marca = None
        producto.talla = recorrertallas(request)
        producto.codigo=request.POST['codigo']
        producto.descripcion=request.POST['descripcion']
        producto.detallesTecnicos=request.POST['tecnicos']
        if request.FILES:
            producto.imagen=request.FILES['imagen']
        producto.save()
        producto.hash = Hash_parse(int(producto.id)+random.randint(1, 1000))
        producto.save()
        if int(request.POST.get("stock"))>0:
            Kardex(producto=producto, tipo="I",cantidad=request.POST.get('stock'),descripcion="Stock inicial debido a registro del producto No. %s"%producto.id).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
        return HttpResponseRedirect("/products/?empresa=%s"%producto.establecimiento_id)
    else:
        return render(request, "producto/crearProducto.html",contexto)


def productos_detalles(request,id):
    producto=Productos.objects.get(id=id)
    if request.POST:
        print(request.POST)
        producto.establecimiento_id=request.POST['establecimiento']
        producto.subcategoria_id=request.POST['categoria']
        producto.nombre = request.POST['nombre']
        producto.tipo = request.POST['tipo']
        if request.POST.get('marca'):
            producto.marca_id=request.POST['marca']
        else:
            producto.marca=None
        producto.talla = recorrertallas(request)
        producto.descripcion=request.POST['descripcion']
        producto.codigo = request.POST['codigo']
        producto.detallesTecnicos=request.POST['tecnicos']
        print(Hash_parse(producto.id))
        if request.FILES:
            producto.imagen=request.FILES['imagen']
        producto.save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha actualizado..!")
    contexto={
        'producto':producto,
        'establecimientos':Establecimiento.objects.filter(usuario=request.user),
        'categorias':Categorias.objects.all(),
        'subcategorias':Subcategorias.objects.all(),
        'marcas':Marca.objects.all(),
        'imagenes':ImagenesProducto.objects.filter(producto_id=id)
    }
    return render(request, 'producto/editarProducto.html',contexto)

def recorrertallas(request):
    valores=''
    for i in request.POST.getlist('talla[]'):
        valores+=i+","
    return (valores)

def registrarColores(request,id):
    if request.POST:
        Colores.objects.create(producto_id=id, codigoColor=request.POST['color'],nombre=request.POST['nombre']).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    return HttpResponseRedirect("/products/edit/%s/"%id)


def eliminarColorProducto(request,id):
    color=Colores.objects.get(id=id)
    producto=color.producto.id
    color.delete()
    messages.add_message(request, messages.ERROR, "El registro se ha eliminado..!")
    return HttpResponseRedirect("/products/edit/%s/"%producto)

def registrarPrecios(request,id):
    web=True
    if request.POST:
        precio=float(str(request.POST['precio']))
        print(request.POST)
        if request.POST.get('web') == 'on':
            web=True
        else:
            web =False
        Precios.objects.create(producto_id=id, precioVenta=precio,detalle=request.POST['detalle'],web=web).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    return HttpResponseRedirect("/products/edit/%s/"%id)

def eliminarPrecios(request,id):
    precio=Precios.objects.get(id=id)
    producto=precio.producto.id
    precio.delete()
    messages.add_message(request, messages.ERROR, "El registro se ha eliminado..!")
    return HttpResponseRedirect("/products/edit/%s/"%producto)


def kardex(request):
    kax=Productos.objects.filter(establecimiento__usuario=request.user)
    if request.GET.get("establecimiento"):
        kax = Productos.objects.filter(establecimiento_id=request.GET.get("establecimiento"))
    contexto={
        'kardex':kax,
        'establecimientos':Establecimiento.objects.filter(usuario=request.user),
    }
    return render(request, "producto/kardex.html",contexto)


def kardex_producto(request,id):
    contexto={
        'kardex':Kardex.objects.filter(producto_id=id),
        'producto':id,
    }
    return render(request, "producto/kardex_producto.html",contexto)

def inventario(request):
    produc=Productos.objects.filter(establecimiento__usuario=request.user)
    if request.GET.get("establecimiento"):
        produc = Productos.objects.filter(establecimiento_id=request.GET.get('establecimiento'))
    if request.POST:
        print(request.POST)
        Kardex(producto_id=request.POST['producto'],tipo=request.POST['tipo'],cantidad=request.POST['cantidad'],descripcion=request.POST['detalle']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado nuevo ingreso en kardex..!")
    contexto={
        'productos':produc,
        'establecimientos':Establecimiento.objects.filter(usuario=request.user)
    }
    return render(request, 'producto/inventario.html',contexto)

def subir_imagenes_producto(request,id):
    if request.POST:
        try:
            img= ImagenesProducto(producto_id=id, imagen=request.FILES['file'],thumbnail=request.FILES['file'])
            img.save()
        except Exception as e:
            print(e)
    return HttpResponse("ok")

def promociones(request):
    promo=Promociones.objects.filter(precio__producto__establecimiento__usuario=request.user)
    produc=Productos.objects.filter(establecimiento__usuario=request.user)
    if request.GET.get('establecimiento'):
        promo=Promociones.objects.filter(precio__producto__establecimiento_id= request.GET.get('establecimiento'))
        produc = Productos.objects.filter(establecimiento_id=request.GET.get('establecimiento'))

    if request.POST:
        Promociones(fechaInicio=request.POST.get('fecha_inicio'),fechaFinal=request.POST.get('fecha_fin'),precio_id=request.POST.get('precio'),
                    descuento=request.POST.get('descuento'),total=request.POST.get('total')).save()
        messages.add_message(request, messages.SUCCESS, "Promoción creada exitosamente.!")
        print(request.POST)

    contexto={
        "establecimientos":Establecimiento.objects.filter(usuario=request.user),
        "promociones":promo,
        "productos":produc
    }
    return render(request, 'Ventas/promociones.html',contexto)

def return_precio_web(request,id):
    precio=Precios.objects.filter(producto_id=id, web=True).first()
    data={
        'id':precio.id,
        'precioTotal':precio.total,
    }
    return JsonResponse(data)

def editarPromocion(request,id):
    promo = Promociones.objects.get(id=id)
    if request.POST:
        promo.fechaInicio=request.POST.get('fecha_inicio')
        promo.fechaFinal=request.POST.get('fecha_fin')
        promo.precio_id = request.POST.get('precio')
        promo.descuento = request.POST.get('descuento')
        promo.total = request.POST.get('total')
        promo.save()
        messages.add_message(request, messages.SUCCESS, "Se ha modificado el registro..!")
    if request.GET.get('establecimiento'):
        return HttpResponseRedirect("/products/promo/?establecimiento=%s" % promo.precio.producto.establecimiento_id)
    else:
        return HttpResponseRedirect("/products/promo/")

def eliminarPromocion(request,id):
    promo =Promociones.objects.get(id=id)
    establecimiento=promo.precio.producto.establecimiento_id
    promo.delete()
    messages.add_message(request, messages.ERROR, "Se ha eliminado el registro..!")
    return HttpResponseRedirect("/products/promo/?establecimiento=%s"%establecimiento)
