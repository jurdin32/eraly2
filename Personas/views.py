from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Empresa.models import Establecimiento
from Home.models import Provincia
from Personas.models import Clientes
from django.contrib import messages

def registroCLientes(request,id=0):
    cliente=Clientes()
    if request.POST:
        if int(id) >0:
            cliente=Clientes.objects.get(id=id)
            messages.add_message(request, messages.SUCCESS, "El registro se ha modificado exitosamente..!")
        else:
            messages.add_message(request, messages.SUCCESS, "El registro se ha creado exitosamente..!")
        cliente.establecimiento_id=request.POST['establecimiento']
        cliente.cedula=request.POST['cedula']
        cliente.nombres=request.POST['nombres']
        cliente.apellidos=request.POST['apellidos']
        cliente.direccion=request.POST['direccion']
        cliente.ciudad_id=request.POST['ciudad']
        cliente.email = request.POST['email']
        cliente.celular=request.POST['celular']
        cliente.telefono=request.POST['telefono']
        cliente.email=request.POST['email']
        cliente.save()

    contexto={
        'clientes':Clientes.objects.filter(establecimiento__usuario=request.user),
        'provincias':Provincia.objects.all(),
        'establecimientos':Establecimiento.objects.filter(usuario=request.user),
    }
    return render(request, 'personas/clientes.html',contexto)

def deshabilitarCliente(request,id):
    cliente=Clientes.objects.get(id=id)
    if cliente.estado:
        cliente.estado=False
        messages.add_message(request, messages.ERROR, "El registro se ha deshabilitado..!")
    else:
        cliente.estado=True
        messages.add_message(request, messages.SUCCESS, "El registro se ha Habilitado..!")
    cliente.save()

    return HttpResponseRedirect("/clients/0/")

