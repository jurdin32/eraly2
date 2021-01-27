from django.shortcuts import render

# Create your views here.
from Personas.models import Clientes


def registroCLientes(request):
    contexto={
        'clientes':Clientes.objects.filter(establecimiento__usuario=request.user)
    }
    return render(request, 'personas/clientes.html',contexto)