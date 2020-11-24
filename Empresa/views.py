from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento


def empresa(request):
    contexto={
        "empresas":Establecimiento.objects.filter(usuario=request.user)
    }
    return render(request, "empresa/empresa.html", contexto)

def registroEmpresa(request):
    contexto={

    }
    return render(request,'empresa/empresa.html',contexto)