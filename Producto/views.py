from django.shortcuts import render
# Create your views here.
from Empresa.models import Establecimiento
from Producto.models import Proveedor


def proveedores(request):
    contexto={
        'establecimientos': Establecimiento.objects.filter(usuario=request.user),
        'proveedores': Proveedor.objects.filter(establecimiento__usuario=request.user)

    }
    return render(request, "producto/proveedores.html",contexto)

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