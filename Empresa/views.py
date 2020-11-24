from http.client import HTTPResponse

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento


def empresa(request):
    if request.POST:
        print(request.POST)
        establecimiento=Establecimiento(usuario=request.user,ruc=request.POST['ruc'],
                        representateLegal=request.POST['representateLegal'],
                        nombreComercial=request.POST['nombreComercial'],
                        descripcion=request.POST['descripcion']
                        )
        establecimiento.save()
    contexto={
        "empresas":Establecimiento.objects.filter(usuario=request.user)
    }
    return render(request, "empresa/empresa.html", contexto)

def eliminar_empresa(request):
    ids=[]
    if(request.GET.get('ids')):
        ids=request.GET['ids'].split()
        for id in ids:
            try:
                Establecimiento.objects.get(id=id).delete()
            except:
                return HttpResponseRedirect("/business/")
    contexto = {
        "empresas": Establecimiento.objects.filter(usuario=request.user)
    }
    return render(request, "empresa/empresa.html", contexto)


def direcciones(request):
    return render(request, "empresa/direcciones.html")