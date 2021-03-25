from django.shortcuts import render

# Create your views here.

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