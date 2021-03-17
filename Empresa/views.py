import datetime
import json

from django.contrib.admin.models import LogEntry
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento, Direccion, UsuarioEmpresa, ConfigurarDocumentos
from Home.models import Provincia


def empresa(request):
    if request.POST:
        print(request.POST)
        establecimiento=Establecimiento.objects.create(usuario=request.user,ruc=request.POST['ruc'],
                        representateLegal=request.POST['representateLegal'],
                        nombreComercial=request.POST['nombreComercial'],
                        descripcion=request.POST['descripcion'],)
        establecimiento.save()
        UsuarioEmpresa(user=request.user, establecimiento=establecimiento,nombreCompleto=request.POST['representateLegal'],cedula=request.POST['ruc']).save()
        ConfigurarDocumentos(establecimiento_id=establecimiento.id, proformas=1, facturas=1).save()
    contexto={
        "empresas":UsuarioEmpresa.objects.filter(user=request.user),
        "logs":LogEntry.objects.filter(user=request.user)
    }
    return render(request, "empresa/empresa.html", contexto)

def modificar_empresa(request,id):
    mensaje=''
    tipo=''
    establecimiento = Establecimiento.objects.get(id=id)
    if request.POST:
        try:
            establecimiento.logo=request.FILES['logo']
            print('viene con logo')
        except:pass
        try:
            print('viene con banner')
            establecimiento.banner=request.FILES['banner']
        except: pass
        try:
            print('viene con pie de pagina')
            establecimiento.pie_pagina=request.FILES['pie']
        except: pass
        try:
            print("viene la cabecera de la tienda")
            establecimiento.cabecera_tienda=request.FILES['cabecera_tienda']
        except:
            pass
        establecimiento.ruc=request.POST['ruc']
        establecimiento.representateLegal=request.POST['representateLegal']
        establecimiento.nombreComercial=request.POST['nombreComercial']
        establecimiento.descripcion=request.POST['descripcion']
        establecimiento.ubicacion_gps = request.POST['ubicacion']
        establecimiento.correo_electronico = request.POST['email']
        establecimiento.web = request.POST['web']
        establecimiento.facebook = request.POST['facebook']
        establecimiento.instagram = request.POST['instagram']
        establecimiento.youtube = request.POST['youtube']
        establecimiento.color_encabezado_documentos=request.POST['color']
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

def eliminar_direcciones(request,id):
    mensaje=""
    tipo=""
    try:
        direccion= Direccion.objects.get(id=id)
        direccion.delete()
        mensaje="El registro se ha eliminado Exitosamente..!"
        tipo="success"
    except:
        pass
    contexto={
       "direcciones":Direccion.objects.filter(establecimiento__usuario=request.user),
        "provincias":Provincia.objects.all(),
        "mensaje":mensaje,
        "tipo":tipo,

    }
    return render(request, "empresa/direcciones.html",contexto)

def subir_logo():
    pass