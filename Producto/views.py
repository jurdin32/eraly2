import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from Home.models import Provincia
from Producto.models import *
from django.contrib import messages
from eraly2.settings import BASE_DIR
from eraly2.snippers import Hash_parse

@login_required(login_url='/store/login/')
def proveedores(request):
    prov=Proveedor.objects.filter(establecimiento__usuarioempresa__user=request.user)
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
        'establecimientos': Establecimiento.objects.filter(usuarioempresa__user=request.user),
        'proveedores': prov,
        'provincias': Provincia.objects.all(),
    }
    return render(request, "producto/proveedores.html",contexto)

@login_required(login_url='/store/login/')
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
        'establecimientos':Establecimiento.objects.filter(usuarioempresa__user=request.user),
        'provincias': Provincia.objects.all(),
    }
    return render(request, "producto/editarProveedores.html",contexto)

@login_required(login_url='/store/login/')
def eliminarProveedor(request,id):
    proveedor=Proveedor.objects.get(id=id)
    proveedor.delete()
    messages.add_message(request, messages.WARNING, "El Proveedor se ha eliminado..!")
    return HttpResponseRedirect('/suppliers/')

@login_required(login_url='/store/login/')
def actividadesProveedor(request,id):
    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        print(request.POST)
        ActividadProveedor.objects.create(proveedor_id=id,nombre=request.POST['nombreActividad'],detalle=request.POST['detalleActividad']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado Nueva actividad del Proveedor..!")
    contexto={
        "proveedor": proveedor,
        'provincias': Provincia.objects.all(),
        'establecimientos': Establecimiento.objects.filter(usuarioempresa__user=request.user),
    }
    return render(request, "producto/editarProveedores.html",contexto)

@login_required(login_url='/store/login/')
def eliminarActividades(request,id):
    actividad=ActividadProveedor.objects.get(id=id)
    proveedor = actividad.proveedor.id
    actividad.delete()
    messages.add_message(request, messages.WARNING, "El registro se ha eliminado..!")
    return HttpResponseRedirect('/suppliers/edit/%s/' % proveedor)

@login_required(login_url='/store/login/')
def tipoProveedor(request,id):
    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        TipoProveedor.objects.create(proveedor_id=id,detalle=request.POST['detalle']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado el nuevo tipo..!")
    contexto = {
        'provincias': Provincia.objects.all(),
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuarioempresa__user=request.user),
    }
    return render(request, "producto/editarProveedores.html", contexto)

@login_required(login_url='/store/login/')
def eliminartipoProveedor(request,id):
    tp=TipoProveedor.objects.get(id=id)
    proveedor=tp.proveedor.id
    tp.delete()
    messages.add_message(request,messages.WARNING,"El registro se ha eliminado..!")
    return HttpResponseRedirect('/suppliers/edit/%s/' % proveedor)

@login_required(login_url='/store/login/')
def direccionProveedor(request,id):
    proveedor = Proveedor.objects.get(id=id)
    if request.POST:
        DireccionProveedor.objects.create(proveedor_id=id,ciudad_id=request.POST['ciudad'],
                                          direccion=request.POST["direccion"],telefono=request.POST['telefono']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado la nueva dirección..!")
    contexto = {
        'provincias': Provincia.objects.all(),
        "proveedor": proveedor,
        'establecimientos': Establecimiento.objects.filter(usuarioempresa__user=request.user),
    }
    return render(request, "producto/editarProveedores.html", contexto)

@login_required(login_url='/store/login/')
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

@login_required(login_url='/store/login/')
def categorias(request):
    cat = Subcategorias.objects.all()
    if request.POST:
        cats=Subcategorias.objects.create(categoria_id=request.POST['categoria'],nombre=request.POST["nombre"])
        cats.save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    contexto={
        'subcategorias':cat,
        'iconos':iconos_text(),
        'establecimientos':Establecimiento.objects.filter(usuarioempresa__user=request.user),
        'categorias':Categorias.objects.all().order_by('nombre')
    }
    return render(request, "producto/categorias.html",contexto)

@login_required(login_url='/store/login/')
def editarCategoria(request,id):
    if request.POST:
        print(request.POST)
        categoria=Subcategorias.objects.get(id=id)
        categoria.categoria_id=request.POST['categoria']
        categoria.nombre=request.POST["nombre"]
        categoria.save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha actualizado..!")
    return  HttpResponseRedirect('/category/')

def subcategorias(request,id):
    if request.POST:
        Subcategorias_2.objects.create(subcategoria_id=id,nombre=request.POST["nombre"]).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    contexto={
        'categoria':Subcategorias.objects.get(id=id),
        'subcategorias':Subcategorias_2.objects.filter(subcategoria_id=id),
    }
    return render(request, "producto/subcategorias.html",contexto)

@login_required(login_url='/store/login/')
def editarSubCategoria(request,id):
    categoria = Subcategorias_2.objects.get(id=id)
    if request.POST:
        categoria.nombre=request.POST["nombre"]
        categoria.save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha actualizado..!")
    return  HttpResponseRedirect('/category/%s'%categoria.subcategoria_id)

#------------ Productos ----------_#
@login_required(login_url='/store/login/')
def productos(request):
    productos=Productos.objects.filter(establecimiento__usuarioempresa__user=request.user)
    if request.GET.get('empresa'):
        productos = Productos.objects.filter(establecimiento_id=request.GET.get('empresa'))

    contexto={
        "productos":productos,
        "empresas":Establecimiento.objects.filter(usuarioempresa__user=request.user)
    }
    return render(request, "producto/productos.html",contexto)

def generarTags(request):
    lista=[]
    if request.session.get('tags'):
        del request.session['tags']
    for tags in Productos.objects.all():
        lista+=tags.etiquetas.split(',')
    lista=set(lista)
    request.session['tags']=lista


@login_required(login_url='/store/login/')
def registarProducto(request):
    generarTags(request)
    producto = Productos()
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
        producto.etiquetas = request.POST['etiquetas']
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
        return HttpResponseRedirect("/products/edit/%s/?precio=on"%str(producto.id))

    contexto = {
        'establecimientos': Establecimiento.objects.filter(usuarioempresa__user=request.user),
        'categorias': Categorias.objects.all().order_by('nombre'),
        'marcas': Marca.objects.all(),
        'subcategorias': Subcategorias.objects.all(),
    }
    return render(request, "producto/crearProducto.html",contexto)

def colores():
    colores = []
    aux=[]
    for color in Colores.objects.all():
        if not color.codigoColor in aux:
            aux.append(color.codigoColor)
            colores.append(color)
    print(colores)
    return colores

@login_required(login_url='/store/login/')
def productos_detalles(request,id):
    generarTags(request)
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
        producto.etiquetas = request.POST['etiquetas']
        producto.detallesTecnicos=request.POST['tecnicos']
        print(Hash_parse(producto.id))
        if request.FILES:
            producto.imagen=request.FILES['imagen']
        producto.save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha actualizado..!")
    print(request.session['tags'])
    contexto={
        'producto':producto,
        'establecimientos':Establecimiento.objects.filter(usuarioempresa__user=request.user),
        'categorias':Categorias.objects.all(),
        'subcategorias':Subcategorias.objects.all(),
        'marcas':Marca.objects.all(),
        'imagenes':ImagenesProducto.objects.filter(producto_id=id),
        'colores':colores(),
    }
    return render(request, 'producto/editarProducto.html',contexto)

def recorrertallas(request):
    valores=''
    for i in request.POST.getlist('talla[]'):
        valores+=i+","
    return (valores)

@login_required(login_url='/store/login/')
def registrarColores(request,id):
    if request.POST:
        Colores.objects.create(producto_id=id, codigoColor=request.POST['color'],nombre=request.POST['nombre']).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    return HttpResponseRedirect("/products/edit/%s/"%id)

@login_required(login_url='/store/login/')
def eliminarColorProducto(request,id):
    color=Colores.objects.get(id=id)
    producto=color.producto.id
    color.delete()
    messages.add_message(request, messages.ERROR, "El registro se ha eliminado..!")
    return HttpResponseRedirect("/products/edit/%s/"%producto)

@login_required(login_url='/store/login/')
def registrarPrecios(request,id):
    web=True
    if request.POST:
        precio=float(str(request.POST['precio']))
        print(request.POST)
        if request.POST.get('web') == 'on':
            web=True
        else:
            web =False
        try:
            preciot=Precios.objects.get(producto_id=id,web=web)
            preciot.web=False
            preciot.save()
            print("se registro")
            Precios.objects.create(producto_id=id, precioVenta=precio, detalle=request.POST['detalle'], web=web).save()
            messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
        except Exception as error:
            print(error)
            Precios.objects.create(producto_id=id, precioVenta=precio,detalle=request.POST['detalle'],web=web).save()
        messages.add_message(request, messages.SUCCESS, "El registro se ha creado..!")
    return HttpResponseRedirect("/products/edit/%s/"%id)

@login_required(login_url='/store/login/')
def eliminarPrecios(request,id):
    precio=Precios.objects.get(id=id)
    producto=precio.producto.id
    precio.delete()
    messages.add_message(request, messages.ERROR, "El registro se ha eliminado..!")
    return HttpResponseRedirect("/products/edit/%s/"%producto)

@login_required(login_url='/store/login/')
def editarPrecios(request,id):
    web=False
    if request.POST:
        if request.POST.get('web') == 'on':
            web=True
        else:
            web =False
        precio=Precios.objects.get(id=id)
        precio.precioVenta=float(str(request.POST['precio']))
        precio.detalle=request.POST['detalle']
        precio.web=web
        precio.save()
        messages.add_message(request, messages.INFO, "El registro se ha actualizado correctamente..!")
        return HttpResponseRedirect("/products/edit/%s/"%precio.producto_id)

@login_required(login_url='/store/login/')
def kardex(request):
    kax=Productos.objects.filter(establecimiento__usuarioempresa__user=request.user)
    if request.GET.get("establecimiento"):
        kax = Productos.objects.filter(establecimiento_id=request.GET.get("establecimiento"))
    contexto={
        'kardex':kax,
        'establecimientos':Establecimiento.objects.filter(usuarioempresa__user=request.user),
    }
    return render(request, "producto/kardex.html",contexto)


@login_required(login_url='/store/login/')
def kardex_producto(request,id):
    contexto={
        'kardex':Kardex.objects.filter(producto_id=id),
        'producto':id,
    }
    return render(request, "producto/kardex_producto.html",contexto)

@login_required(login_url='/store/login/')
def inventario(request):
    produc=Productos.objects.filter(establecimiento__usuarioempresa__user=request.user)
    if request.GET.get("establecimiento"):
        produc = Productos.objects.filter(establecimiento_id=request.GET.get('establecimiento'))
    if request.POST:
        print(request.POST)
        Kardex(producto_id=request.POST['producto'],tipo=request.POST['tipo'],cantidad=request.POST['cantidad'],descripcion=request.POST['detalle']).save()
        messages.add_message(request, messages.SUCCESS, "Se ha registrado nuevo ingreso en kardex..!")
    contexto={
        'productos':produc,
        'establecimientos':Establecimiento.objects.filter(usuarioempresa__user=request.user)
    }
    return render(request, 'producto/inventario.html',contexto)

@login_required(login_url='/store/login/')
def subir_imagenes_producto(request,id):
    if request.POST:
        try:
            img= ImagenesProducto(producto_id=id, imagen=request.FILES['file'],thumbnail=request.FILES['file'])
            img.save()
        except Exception as e:
            print(e)
    return HttpResponse("ok")

def eliminar_imagen(reqeust,id):
    id_producto=0
    try:
        img = ImagenesProducto.objects.get(id=id)
        id_producto=img.producto_id
        img.delete()
        messages.add_message(reqeust,messages.INFO, 'Se eliminó la imágen seleccionada..!')
    except:
        pass
    return HttpResponseRedirect("/products/edit/%s/"%str(id_producto))


@login_required(login_url='/store/login/')
def promociones(request):
    promo=Promociones.objects.filter(precio__producto__establecimiento__usuarioempresa__user=request.user)
    produc=Productos.objects.filter(establecimiento__usuarioempresa__user=request.user,precios__web=True)

    if request.GET.get('establecimiento'):
        promo=Promociones.objects.filter(precio__producto__establecimiento_id= request.GET.get('establecimiento'))
        produc = Productos.objects.filter(establecimiento_id=request.GET.get('establecimiento'),precios__web=True)

    if request.POST:
        Promociones(fechaInicio=request.POST.get('fecha_inicio'),fechaFinal=request.POST.get('fecha_fin'),precio_id=request.POST.get('precio'),
                    descuento=request.POST.get('descuento'),total=request.POST.get('total')).save()
        messages.add_message(request, messages.SUCCESS, "Promoción creada exitosamente.!")
        print(request.POST)

    contexto={
        "establecimientos":Establecimiento.objects.filter(usuarioempresa__user=request.user),
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

@login_required(login_url='/store/login/')
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

@login_required(login_url='/store/login/')
def eliminarPromocion(request,id):
    promo =Promociones.objects.get(id=id)
    establecimiento=promo.precio.producto.establecimiento_id
    promo.delete()
    messages.add_message(request, messages.ERROR, "Se ha eliminado el registro..!")
    return HttpResponseRedirect("/products/promo/?establecimiento=%s"%establecimiento)
