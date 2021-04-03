from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from future.backports import datetime

from Empresa.views import direcciones
from Home.models import Provincia, Pais
from Personas.models import *
from Producto.models import Productos, Categorias, CalificacionProductos, Promociones, Precios
from django.contrib import messages

from Store.models import Publicidad


def tienda(request):
    productos=Productos.objects.filter(precios__web=True)
    puntuados = productos.filter(puntuacion__range=(2, 5)).order_by('-puntuacion')
    paginator = Paginator(puntuados, 9)
    page = request.GET.get('page')
    contexto={
        'categorias':Categorias.objects.all().order_by('nombre'),
        'productos':productos.order_by('id'), # deben ir los destacados, los de mas puntuación,
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
    producto = Productos.objects.get(hash=request.GET.get('hash'))
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
        'productos':Productos.objects.filter(subcategoria=producto.subcategoria,precios__web=True),
        'imagnes':Publicidad.objects.filter(estado=True),
    }
    return render(request, 'Store/demo-shop-8-product-details.html', contexto)

def add_carrito(request):
    promocion=None
    descuento_promo = 0
    producto=Productos.objects.get(id=request.GET.get('producto'))
    if request.GET.get('promocion'):
        if int(request.GET.get('promocion'))>0:
            promocion =Promociones.objects.get(id=request.GET.get('promocion'))
            descuento_promo=promocion.descuento
    cantidad = request.GET.get('cantidad')
    precio = Precios.objects.filter(producto_id=producto.id,web=True).last()
    precio=float(precio.total)
    descuento = precio * (float(descuento_promo)/100)
    precioU = precio-descuento
    total =precioU * float(request.GET.get('cantidad'))
    #del request.session['carrito']
    cart = {}
    if not request.session.get('carrito'):
        request.session['carrito']=[]
    cart.setdefault('producto_id',producto.id)
    cart.setdefault('producto_nombre',producto.nombre)
    imagen=""
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



def _tiendas(request):
    contexto={

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

    contexto={
        'direccion':direccionesW
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


def ver_subcategorias(request):
    prod=Productos.objects.filter(precios__web=True)
    paginator=None
    min=0
    max =0
    if request.GET.get('subcategoria'):
        prod=prod.filter(subcategoria_id=request.GET.get('subcategoria'))
    elif request.GET.get('categoria'):
        prod=prod.filter(subcategoria__categoria_id=request.GET.get('categoria'))

    if request.GET.get('size'):

        prod=prod.filter(talla__icontains=request.GET.get('size'))

    if request.GET.get('bprecio'):
        valores=request.GET.get("bprecio").split(",")
        nueva_lista = [sublista for sublista in valores if sublista]
        print(nueva_lista)
        if len(nueva_lista)==2:
            min = nueva_lista[0].replace(",",".")
            max= nueva_lista[1].replace(",",".")
        else:
            min=max =nueva_lista[0]
        prod=prod.filter(precios__total__range=(float(min),float(max)))

    if request.GET.get("list"):
        paginator = Paginator(prod, request.GET.get("list"))
    else:
        paginator = Paginator(prod, 12)

    page = request.GET.get('page')

    contexto={
        'productos':paginator.get_page('page'),
        'categorias':Categorias.objects.all(),
        'numero':request.GET.get("list"),
        'min':min,
        'max':max,
    }

    if request.GET.get('grid'):
        return render(request, 'Store/demo-shop-8-category-4col.html', contexto)
    else:
        return render(request, 'Store/demo-shop-8-category-list.html', contexto)


def register(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-register.html', contexto)



def checkout(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-checkout.html', contexto)



def contact(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-contact-us.html', contexto)




def ejemplo(request):
    contexto={

    }
    return render(request, 'Store/ejemplo.html', contexto)