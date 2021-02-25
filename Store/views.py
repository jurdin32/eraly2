from django.shortcuts import render

# Create your views here.

def tienda(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8.html',contexto)

def eproductos(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-category-4col.html', contexto)

def edetalles(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8-product-details.html', contexto)