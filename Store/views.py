from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from simple_search import search_filter
# Create your views here.
from future.backports import datetime

from Home.models import Provincia
from Personas.models import *
from Producto.models import Productos, Categorias, CalificacionProductos, Promociones, Precios, Colores
from django.contrib import messages

from Store.models import Publicidad, ComprasWeb, DetalleCompraWeb, Favoritos
from eraly2.snippers import Hash_parse


def tienda(request):
    productos=Productos.objects.filter(precios__web=True)
    puntuados = productos.filter(puntuacion__range=(2, 5)).order_by('-puntuacion')
    if request.session.get('tiendas'):
        del request.session['tiendas']
    request.session['tiendas']=[{"id":tienda.id,"nombre":tienda.nombreComercial,'slug':tienda.slug} for tienda in Establecimiento.objects.filter(activo=True).order_by('slug')]
    print(request.session['tiendas'])
    paginator = Paginator(puntuados, 20)
    page = request.GET.get('page')
    contexto={
        'categorias':Categorias.objects.all().order_by('nombre'),
        'productos':productos.order_by('-id'), # deben ir los destacados, los de mas puntuación,
        'puntuados':paginator.get_page(page),
        'nuevos':productos.filter(puntuacion__range=(0,2)).order_by('-puntuacion'),

    }
    return render(request, 'Store/demo-shop-8.html',contexto)

def _productos(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-category-4col.html', contexto)

def _detalles(request):
    fecha = datetime.datetime.now().date()
    productoss = Productos.objects.filter(precios__web=True)
    producto = productoss.get(hash=request.GET.get('hash'))
    promo =Promociones.objects.filter(precio__producto=producto).last()
    if promo:
        if fecha >= promo.fechaInicio and fecha <= promo.fechaFinal:
            print("Hay promocion")
        else:
            promo=None
    if request.POST:
        if request.user.is_authenticated:
            cal = CalificacionProductos.objects.filter(usuario=request.user, producto=producto).exists()
            if not cal:
                CalificacionProductos(producto=producto,rating=request.POST['rata'],comentario=request.POST['comentario'],usuario=request.user).save()
                rating = CalificacionProductos.objects.filter(producto=producto).aggregate(rating=Avg('rating'))
                producto.puntuacion = float(rating['rating'])
                producto.save()
                messages.add_message(request, messages.SUCCESS, "Gracias por calificar este producto..!")
            else:
                messages.add_message(request, messages.ERROR, "Usted ya calificó este producto.!")
        else:
            return HttpResponseRedirect("/store/login/")
    contexto={
        'producto':producto,
        'calificaciones': CalificacionProductos.objects.filter(producto_id=producto.id),
        'promocion':promo,
        'productos':productoss.filter(subcategoria=producto.subcategoria),
        'imagnes':Publicidad.objects.filter(estado=True),
        'categorias': Categorias.objects.all().order_by('nombre'),
    }
    return render(request, 'Store/demo-shop-8-product-details.html', contexto)

def add_carrito(request):
    promocion=None
    descuento_promo = 0
    color=None
    imagen = ""
    talla=None
    producto=Productos.objects.get(id=request.GET.get('producto'))
    if request.GET.get('promocion'):
        if int(request.GET.get('promocion'))>0:
            promocion =Promociones.objects.get(id=request.GET.get('promocion'))
            descuento_promo=promocion.descuento
    if request.GET.get('color'):
        color= request.GET.get('color')
    cantidad = request.GET.get('cantidad')
    precio = Precios.objects.filter(producto_id=producto.id,web=True).last()
    precio=float(precio.precioVenta)
    descuento = precio * (float(descuento_promo)/100)
    precioU = precio-descuento
    total =precioU * float(request.GET.get('cantidad'))
    #del request.session['carrito']
    cart = {}
    if not request.session.get('carrito'):
        request.session['carrito']=[]
    cart.setdefault('producto_id',producto.id)
    cart.setdefault('producto_nombre',producto.nombre)

    if request.GET.get('color'):
        color=Colores.objects.get(id= request.GET.get('color')).nombre
    if request.GET.get('talla'):
        talla=request.GET.get('talla')

    try:
        imagen = producto.imagen.name
    except:
        if producto.imagenesproducto_set.first():
            imagen = producto.imagenesproducto_set.first().imagen
        else:
            imagen=""

    cart.setdefault('producto_imagen',imagen)
    cart.setdefault('hash',producto.hash)
    cart.setdefault('precio_normal',round(precio,2))
    cart.setdefault('descuento_porcentaje',descuento_promo)
    cart.setdefault('precio_promocion',round(precioU,2))
    cart.setdefault('cantidad',cantidad)
    cart.setdefault('precio_total',round(total,2))
    cart.setdefault('color',color)
    cart.setdefault('talla', talla)

    if control_carrito(request,producto_id=producto.id):
        request.session['carrito'].append(cart)
        request.session.save()
        return JsonResponse(cart)
    else:
        cart = {'producto_id': 0}
        return JsonResponse(cart)


def control_carrito(request,producto_id):
    if request.session.get('carrito'):
        for c in request.session.get('carrito'):
            print(int(dict(c)['producto_id']))
            if int(producto_id) == int(dict(c)['producto_id']):
                print("no se agrega porque ya existe")
                return False
    return True

def deleteItem(request,producto_id):
    for item in request.session.get('carrito'):
        if producto_id == item['hash']:
            request.session.get('carrito').remove(item)
            request.session.save()

def eliminar_item(request):
    print(request.GET.get('product_id'))
    producto_id=request.GET.get('product_id')

    if request.session.get('carrito'):
        if request.GET.get('cc'):
            print("entro aqui",request.GET)
            deleteItem(request, producto_id)
            return HttpResponseRedirect("/store/view/cart/")
        else:
            deleteItem(request,producto_id)
            return HttpResponseRedirect('/store/details/?hash=%s'%producto_id)

def modificar_carrito(request,cantidad):
    for c in request.session.get('carrito'):
        if request.GET.get('hash') == dict(c)['hash']:
            cantidad = cantidad
            precio = float(c['precio_normal'])
            descuento = precio * (float(c['descuento_porcentaje']) / 100)
            precioU = precio - descuento
            total = precioU * float(cantidad)
            c['precio_normal']= round(precio,2)
            c['precio_promocion']= round(precioU,2)
            c['cantidad']= cantidad
            c['precio_total']= round(total,2)
            request.session.save()
            return c

def ver_cart(request):
    if request.GET.get('add'):
        item=modificar_carrito(request,request.GET.get('add'))
        return JsonResponse(item)

    if request.GET.get('remove'):
        item=modificar_carrito(request,request.GET.get('remove'))
        return JsonResponse(item)
    return render(request,'Store/demo-shop-8-cart.html')

def vaciar_carrito(request):
    if request.session.get('carrito'):
        del request.session['carrito']
        messages.add_message(request, messages.SUCCESS, "El carrito esta vacio..!")
    return HttpResponseRedirect("/store/view/cart/")

#obtiene las categorias por establecimiento:
def _obtener_categoria(id):
    categorias =[]
    aux=[]
    for prod in Productos.objects.filter(establecimiento_id=id):
        if not prod.subcategoria.subcategoria.id in aux:
            aux.append(prod.subcategoria.subcategoria.id)
            categorias.append({'id':prod.subcategoria.subcategoria.id,'nombre':prod.subcategoria.subcategoria.nombre,'imagen':prod.imagen,'subcat':prod.subcategoria.subcategoria.id},)
    print(categorias)
    return categorias

def _tiendas(request,slug):
    establecimiento=Establecimiento.objects.get(slug=slug)
    productos=Productos.objects.filter(establecimiento=establecimiento,precios__web=True).order_by('puntuacion')
    contexto={
        'categorias':Categorias.objects.all(),
        'tienda':establecimiento,
        'categoriaTiendas':_obtener_categoria(establecimiento.id),
        'contador':len(_obtener_categoria(establecimiento.id)),
        'pestrella':productos,
        'de4y5':productos.filter(puntuacion__range=(4,5)),
        'imagnes':Publicidad.objects.all(),
    }
    return render(request, 'Store/tiendas.html', contexto)

@login_required(login_url='/store/login/')
def account(request):
    usuario=None
    try:
        usuario = UsuariosWeb.objects.get(usuario=request.user)
    except:
        usuario =UsuariosWeb.objects.create(usuario=request.user)
        usuario.save()
    if request.POST:
        user = request.user
        if user.check_password(request.POST.get('password')):
            user.first_name=request.POST.get('nombres')
            user.last_name=request.POST.get('apellidos')
            user.email=request.POST.get('email')
            usuario.identificacion = request.POST.get('identificacion')
            usuario.save()
            print( request.POST )
            if request.POST.get('cambiar')=='1' and len(request.POST.get('password1'))>0 and len(request.POST.get('password2')):
                if request.POST.get('password1')==request.POST.get('password2'):
                    user.set_password(request.POST.get('password2'))
            user.save()
            messages.add_message(request, messages.SUCCESS, "Tú información de contacto se actualizó correctamente..!")
        else:
            messages.add_message(request, messages.ERROR, "Lo sentimos.! no es posible actualizar los datos, es posible que la contraseña ingresada no sea correcta, Reintente")

    contexto={
        'usuario':usuario,
        'categorias':Categorias.objects.all()
    }
    return render(request, 'Store/demo-shop-8-myaccount.html', contexto)

@login_required(login_url='/store/login/')
def dashboard(request):
    usuario = None
    direccionesW=None
    try:
        usuario = UsuariosWeb.objects.get(usuario=request.user)
    except:
        usuario = UsuariosWeb.objects.create(usuario=request.user)
        usuario.identificacion=str.zfill(str(usuario.id),10)
        usuario.save()
    try:
        direccionesW = DireccionesWeb.objects.get(usuarioWeb=usuario, envio=True)
    except:
        pass
    if request.session.get('tiendas'):
        del request.session['tiendas']
    request.session['tiendas']=[{"id":tienda.id,"nombre":tienda.nombreComercial,'slug':tienda.slug} for tienda in Establecimiento.objects.all().order_by('slug')]

    contexto={
        'direccion':direccionesW,
        'categorias': Categorias.objects.all()
    }
    return render(request, 'Store/demo-shop-8-dashboard.html', contexto)

@login_required(login_url='/store/login/')
def directorio(request):
    envio =False
    usuario =None
    try:
        usuario=UsuariosWeb.objects.get(usuario=request.user)
    except:
        usuario = UsuariosWeb.objects.create(usuario=request.user)

    if request.POST:
        if request.POST.get('envio')=="on":
            envio=True
            for direcc  in DireccionesWeb.objects.filter(usuarioWeb=usuario):
                direcc.envio=False
                direcc.save()

        if request.GET.get('edit'):
            direccion=DireccionesWeb.objects.get(id=request.GET.get('edit'))
            direccion.direccion= request.POST.get('direccion')
            direccion.ciudad_id=request.POST.get('ciudad')
            direccion.envio=envio
            direccion.telefono=request.POST.get('telefono')
            direccion.celular=request.POST.get('celular')
            direccion.observacion=request.POST.get('observacion')
            direccion.save()
            messages.add_message(request, messages.SUCCESS, "Se modificó el directorio..!")
            return HttpResponseRedirect("/store/directory/")
        else:
            direccion=DireccionesWeb.objects.create(usuarioWeb=usuario, direccion=request.POST.get('direccion'), ciudad_id=request.POST.get('ciudad'),
                                      envio=envio, telefono=request.POST.get('telefono'),celular=request.POST.get('celular'),
                                                observacion=request.POST.get('observacion'))
            direccion.save()
            messages.add_message(request, messages.SUCCESS, "Se agrego nueva dirección al directorio..!")
    contexto={
        'provincias':Provincia.objects.all(),
        'direcciones':DireccionesWeb.objects.filter(usuarioWeb=usuario),
        'categorias': Categorias.objects.all()
    }
    return render(request, 'Store/demo-shop-8-directory.html', contexto)

def eliminar_directorio(request,n):
    try:
        direct=DireccionesWeb.objects.get(id=n)
        direct.delete()
        messages.add_message(request, messages.ERROR, "Se eliminó el registro..!")
        return HttpResponseRedirect("/store/directory/")
    except:
        return  HttpResponseRedirect("/store/directory/")

def pagos(request):
    contexto={

    }
    return render(request,'Store/demo-shop-8-pay_information.html',contexto)



def obtenerColores():
    colores=[]
    for color in Colores.objects.all():
        code=color.codigoColor.replace("#","")
        if not code in colores:
            colores.append(code)
    return set(colores)

def ver_subcategorias(request):
    prod=Productos.objects.filter(precios__web=True)
    paginator=None
    cat=None
    min=0
    max =0
    excento=0
    q=''
    ord=''

    if request.GET.get('ctgry'):
        prod = prod.filter(subcategoria__subcategoria__categoria_id=request.GET.get('ctgry'))
        cat = Categorias.objects.get(id=request.GET.get('ctgry'))
        excento = 1

    if request.GET.get('subcategoria'):
        prod=prod.filter(subcategoria__subcategoria_id=request.GET.get('subcategoria'))

    elif request.GET.get('categoria'):
        prod=prod.filter(subcategoria__subcategoria__categoria_id=request.GET.get('categoria'))
        cat= Categorias.objects.get(id=request.GET.get('categoria'))
        excento =1


    if request.GET.get('size'):
        prod=prod.filter(talla__icontains=request.GET.get('size'))

    if request.GET.get('color'):
        prod=prod.filter(colores__codigoColor="#"+request.GET.get('color'))

    if request.GET.get("q"):
        q=request.GET.get("q")
        search_fields = ['nombre', 'subcategoria__nombre', 'etiquetas','marca__nombre','establecimiento__nombreComercial','descripcion','detallesTecnicos']
        prod = prod.filter(search_filter(search_fields, q))

    if request.GET.get("ord"):
        if request.GET.get("ord") == "name":
            prod = prod.order_by('nombre')
        elif request.GET.get("ord") == "star":
            prod = prod.order_by('-puntuacion')
        else:
            prod = prod.order_by('precios__total')
        ord=request.GET.get("ord")

    if request.GET.get('bprecio'):
        valores=request.GET.get("bprecio").split(",")
        nueva_lista = [sublista for sublista in valores if sublista]
        if len(nueva_lista)==2:
            min = nueva_lista[0].replace(",",".")
            max= nueva_lista[1].replace(",",".")
        else:
            min=max =nueva_lista[0]
        prod=prod.filter(precios__total__range=(float(min),float(max)))

    prod = prod.order_by('-puntuacion')
    if request.GET.get("list"):
        paginator = Paginator(prod, request.GET.get("list"))
    else:
        paginator = Paginator(prod, 12)


    page = request.GET.get('page')
    contexto={
        'productos':paginator.get_page(page),
        'categorias':Categorias.objects.all().order_by('nombre'),
        'numero':request.GET.get("list"),
        'min':min,
        'max':max,
        'categoria':cat,
        'excento':excento,
        'colores': obtenerColores(),
        'q':q,
        'ord':ord,
    }

    if request.GET.get('grid'):
        return render(request, 'Store/demo-shop-8-category-4col.html', contexto)
    else:
        return render(request, 'Store/demo-shop-8-category-list.html', contexto)




def register(request):
    mensaje=""
    error=""
    if request.POST:
        nombres= request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        ussuario=nombres[0:3]+apellidos[0:3]+str(datetime.datetime.now()).replace("-","").replace(" ","").replace(".","").replace(":","")
        try:
            uuuu=User.objects.get(email=request.POST.get("email"))
            print(uuuu)
            error = "No es posible realizar el registro, Esta dirección ya se uso por otro usuario,si no recuerda su contraseña puede cambiarla desde "
        except Exception as ex:
            if request.POST.get("password1") == request.POST.get('password2'):
                user=User.objects.create(username=ussuario,email=request.POST.get('email'),
                                         first_name=request.POST.get('nombres'),last_name=request.POST.get('apellidos'),
                                         is_active=True,is_staff=False,is_superuser=False)
                user.set_password(request.POST.get('password2'))
                user.save()
                UsuariosWeb.objects.create(usuario=user,identificacion="0000000000000").save()
                mensaje="Su registro se ha creado de manera exitosa, puede iniciar sesión en el siguiente enlace:"
        print(request.POST)
    contexto={
        'mensaje':mensaje,
        'error':error,
    }
    return render(request, 'Store/demo-shop-8-register.html', contexto)



def checkout(request):
    contexto={
        'direcciones':DireccionesWeb.objects.get(envio=True,usuarioWeb__usuario=request.user)
    }
    return render(request, 'Store/demo-shop-8-checkout.html', contexto)

@login_required(login_url='/store/login/')
def pay(request):
    totalCarrito=0
    compra=None
    usuario=UsuariosWeb.objects.get(usuario=request.user)
    try:
        for car in request.session['carrito']:
            totalCarrito+=float(car['precio_total'])
            print(car)
        compra= ComprasWeb.objects.create(usuario=usuario, subtotal=totalCarrito, por_confirmar=True)
        compra.save()
        compra.hash= Hash_parse(str(compra.id))
        compra.save()
        for car in request.session['carrito']:
            detalle=DetalleCompraWeb.objects.create(compra=compra, producto_id=car['producto_id'],precio_normal=car['precio_normal'],
                                                    descuento_porcentaje=car['descuento_porcentaje'],precio_promocion=car['precio_promocion'],
                                                    cantidad=car['cantidad'],precio_total=car['precio_total'],color=car['color'],talla=car['talla'])
            detalle.save()
        del request.session['carrito']
    except:
        return HttpResponseRedirect("/store/dashboard/")

    contexto={
        'compra':compra
    }
    return render(request,'Store/demo-shop-8-pay.html',contexto)

@login_required(login_url='/store/login/')
def misOrdenes(request):
    usuario=request.user.usuariosweb_set.first()
    ordenes=None
    orden=None
    ordenesss=None
    if request.GET.get("order"):
        orden= ComprasWeb.objects.get(hash=request.GET.get("order"))
    else:
        ordenes=ComprasWeb.objects.filter(usuario=usuario).order_by('-id')
        paginator = Paginator(ordenes, 10)
        page = request.GET.get('page')
        ordenesss=paginator.get_page(page)

    contexto={
        'ordenes':ordenesss,
        'orden':orden,
        'categorias': Categorias.objects.all()
    }
    if request.GET.get("order"):
        return render(request, 'Store/demo-shop-8-orders-detail.html', contexto)
    return render(request,'Store/demo-shop-8-orders.html',contexto)

def contact(request):
    contexto={
        'categorias': Categorias.objects.all(),
    }
    return render(request, 'Store/demo-shop-8-contact-us.html', contexto)

@login_required(login_url='/store/login/')
def favoritos(request):
    print(request.GET.get('hash'))
    producto=Productos.objects.get(hash=request.GET.get('hash'))
    print(producto)
    isp=False
    usuarioweb=UsuariosWeb.objects.get(usuario=request.user)
    try:
        Favoritos.objects.get(usuario=usuarioweb,producto=producto)
        isp =True
    except Favoritos.DoesNotExist:
        isp=False
    if not isp:
        favorito= Favoritos.objects.create(usuario=usuarioweb,producto_id=producto.id)
        favorito.save()
        messages.add_message(request,messages.SUCCESS, "Se ha agregó a tus favoritos..!")
    else:
        messages.add_message(request,messages.WARNING, 'El producto ya está en favoritos')

    return HttpResponseRedirect("/store/details/?hash=%s"%request.GET.get('hash'))

@login_required(login_url='/store/login/')
def lista_favoritos(request):
    usuariow=UsuariosWeb.objects.get(usuario=request.user)
    contexto={
        'favoritos':Favoritos.objects.filter(usuario=usuariow)
    }

    return render(request, 'Store/demo-shop-8-wishlist.html',contexto)

@login_required(login_url='/store/login/')
def borrar_favoritos(request,slug):
    usuariow = UsuariosWeb.objects.get(usuario=request.user)
    try:
        favoritos=Favoritos.objects.get(usuario=usuariow,producto__hash=slug)
        favoritos.delete()
        messages.add_message(request,messages.ERROR,"El producto se eliminó de su lista de deseos..!")
    except Favoritos.DoesNotExist:
        pass
    return HttpResponseRedirect("/store/wishlist/")

def ejemplo(request):
    contexto={

    }
    return render(request, 'Store/ejemplo.html', contexto)