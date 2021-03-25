from django.db.models import Avg
from django.shortcuts import render

# Create your views here.
from Producto.models import Productos, Categorias, CalificacionProductos
from django.contrib import messages

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
    producto = Productos.objects.get(hash=request.GET.get('hash'))
    if request.POST:
        CalificacionProductos(producto=producto,rating=request.POST['rata'],comentario=request.POST['comentario'],usuario=request.user).save()
        rating = CalificacionProductos.objects.filter(producto=producto).aggregate(rating=Avg('rating'))
        producto.puntuacion = float(rating['rating'])
        producto.save()
        messages.add_message(request, messages.SUCCESS, "Gracias por calificar este producto..!")

    contexto={
        'producto':producto,
        'calificaciones': CalificacionProductos.objects.filter(producto_id=producto.id)
    }
    return render(request, 'Store/demo-shop-8-product-details.html', contexto)

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