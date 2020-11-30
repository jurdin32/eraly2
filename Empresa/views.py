import json

from django.core import serializers
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento, Direccion, UsuarioEmpresa
from Home.models import Pais, Ciudad, Provincia


def empresa(request):
    if request.POST:
        print(request.POST)
        establecimiento=Establecimiento.objects.create(usuario=request.user,ruc=request.POST['ruc'],
                        representateLegal=request.POST['representateLegal'],
                        nombreComercial=request.POST['nombreComercial'],
                        descripcion=request.POST['descripcion']

                        )
        establecimiento.save()
        UsuarioEmpresa(user=request.user, establecimiento=establecimiento,nombreCompleto=request.POST['representateLegal'],cedula=request.POST['ruc']).save()
    contexto={
        "empresas":UsuarioEmpresa.objects.filter(user=request.user)
    }
    return render(request, "empresa/empresa.html", contexto)

def modificar_empresa(request,id):
    mensaje=''
    tipo=''
    if request.POST:
        establecimiento= Establecimiento.objects.get(id=id)
        establecimiento.ruc=request.POST['ruc']
        establecimiento.representateLegal=request.POST['representateLegal']
        establecimiento.nombreComercial=request.POST['nombreComercial']
        establecimiento.descripcion=request.POST['descripcion']
        establecimiento.save()
        usuarioEstablecimiento= UsuarioEmpresa.objects.get(establecimiento=establecimiento)
        usuarioEstablecimiento.nombreCompleto=request.POST['representateLegal']
        usuarioEstablecimiento.cedula=request.POST['ruc']
        establecimiento.save()
        mensaje="El registro fue modificado exitosamente..!"
        tipo="success"
    contexto={
        "establecimiento":Establecimiento.objects.get(id=id),
        "mensaje":mensaje,
        "tipo":tipo,
        "provincias":Provincia.objects.all()
    }
    return render(request, 'empresa/editarEmpresa.html',contexto)

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

def crear_direcciones(request,idEmpresa):
    Direccion.objects.create(establecimiento_id=idEmpresa,ciudad_id=request.POST['ciudad'],direccion=request.POST['direccion'],telefono=request.POST['telefono']).save()
    return HttpResponseRedirect("/business/edit/%s/"%idEmpresa)

def direcciones(request):
    contexto={
       "direcciones":Direccion.objects.filter(establecimiento__usuario=request.user),
        "provincias":Provincia.objects.all(),
    }
    return render(request, "empresa/direcciones.html",contexto)

def modificar_direcciones(request,id):
    mensaje=""
    tipo=""
    if request.POST:
        direccion=Direccion.objects.get(id=id)
        direccion.ciudad_id=request.POST['ciudad']
        direccion.telefono=request.POST['telefono']
        direccion.direccion=request.POST['direccion']
        direccion.save()
        mensaje="El registro de direcciones fue modificado existosamente..!"
        tipo="success"
    contexto={
       "direcciones":Direccion.objects.filter(establecimiento__usuario=request.user),
        "provincias":Provincia.objects.all(),
        "mensaje":mensaje,
        "tipo": tipo,
    }
    return render(request, "empresa/direcciones.html",contexto)