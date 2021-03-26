from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from future.backports import datetime

from Producto.models import Productos, Categorias, CalificacionProductos, Promociones, Precios
from django.contrib import messages

from Store.models import Publicidad


datos=[]

def tienda(request):
    contexto={
        'categorias':Categorias.objects.all().order_by('nombre'),
        'productos':Productos.objects.all().order_by('id') # deben ir los destacados, los de mas puntuación

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
        print("Fecha inicio",promo.fechaInicio)
        print('Fecha final',promo.fechaFinal)
        print('fecha actual',fecha)
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
        promocion =Promociones.objects.get(id=request.GET.get('promocion'))
        descuento_promo=promocion.descuento

    cantidad = request.GET.get('cantidad')
    precio = Precios.objects.filter(producto_id=producto.id,web=True).last()
    precio=float(precio.total)
    descuento = precio * (float(descuento_promo)/100)
    precioU = precio-descuento
    total =precioU * float(request.GET.get('cantidad'))

    cart={
        'producto_id':producto.id,
        'producto_nombre':producto.nombre,
        'producto_imagen':producto.imagen.name or producto.imagenesproducto_set.first().imagen.name,
        'hash':producto.hash,
        'precio_normal':precio,
        'descuento_porcentaje':descuento_promo,
        'precio_promocion':precioU,
        'cantidad':cantidad,
        'precio_total': total,
    }
    if not cart in datos:
        datos.append(cart)
    request.session['carrito']=datos
    request.session.save()

    print("sesion",request.session['carrito'])
    return JsonResponse(cart)



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