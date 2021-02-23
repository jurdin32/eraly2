from django.shortcuts import render

# Create your views here.

def tienda(request):
    contexto={

    }
    return render(request, 'Store/demo-shop-8.html',contexto)