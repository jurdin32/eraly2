from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from future.backports import datetime

from Producto.models import Productos, Categorias, CalificacionProductos, Promociones, Precios
from django.contrib import messages

from Store.models import Publicidad


def tienda(request):
    contexto={
        'categorias':Categorias.objects.all().order_by('nombre'),
        'productos':Productos.objects.all().order_by('id') # deben ir los destacados, los de mas puntuación,

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
        'productos':Productos.objects.filter(subcategoria=producto.subcategoria),
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
    cart.setdefault('producto_imagen',producto.imagen.name or producto.imagenesproducto_set.first().imagen.name)
    cart.setdefault('hash',producto.hash)
    cart.setdefault('precio_normal',precio)
    cart.setdefault('descuento_porcentaje',descuento_promo)
    cart.setdefault('precio_promocion',precioU)
    cart.setdefault('cantidad',cantidad)
    cart.setdefault('precio_total',total)
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

def eliminar_item(request):
    print(request.GET.get('product_id'))
    producto_id=request.GET.get('product_id')
    hash=""
    print(request.GET)
    print(request.get_full_path())
    if request.session.get('carrito'):
        for item in request.session.get('carrito'):
            if producto_id == item['hash']:
                request.session.get('carrito').remove(item)
                print(item['hash'])
                hash =item['hash']
                request.session.save()
                print(request.session.get('carrito'))
                messages.add_message(request, messages.ERROR, "Se eliminó del carrito..!")
                return HttpResponseRedirect('/store/details/?hash=%s'%hash)

def ver_cart(request):

    return render(request,'Store/demo-shop-8-cart.html')


def _tiendas(request):
    contexto={

    }
    return render(request, 'Store/tiendas.html', contexto)

def account(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-myaccount.html', contexto)

def dashboard(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-dashboard.html', contexto)

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