from django.shortcuts import render

# Create your views here.
def proformas(request):
    contexto={

    }
    return render(request, 'Ventas/proformas.html', contexto)