import json

from django.core import serializers
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento, Direccion


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

def modificar_empresa(request,id):
    if request.POST:
        print(request.POST)
    contexto={
        "establecimiento":Establecimiento.objects.get(id=id)
    }
    return render(request, 'empresa/editarEmpresa.html')

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
    contexto={
       "direcciones":Direccion.objects.filter(establecimiento__usuario=request.user)
    }
    return render(request, "empresa/direcciones.html",contexto)