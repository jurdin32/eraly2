from django.shortcuts import render
# Create your views here.
def proveedores(request):
    contexto={

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