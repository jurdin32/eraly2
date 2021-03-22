from django.shortcuts import render

# Create your views here.
from Producto.models import Productos


def tienda(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8.html',contexto)

def _productos(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-category-4col.html', contexto)

def _detalles(request):
    contexto={
        'producto':Productos.objects.get(hash=request.GET.get('hash'))
    }
    return render(request, 'Store/demo-shop-8-product-details.html', contexto)

def _tiendas(request):
    contexto={

    }
    return render(request, 'Store/tiendas.html', contexto)

def ejemplo(request):
    contexto={

    }
    return render(request, 'Store/ejemplo.html', contexto)