from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
# Create your views here.
from Empresa.models import Establecimiento, UsuarioEmpresa
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

def registro_otrosUsuarios(request):
    if request.POST:
        nombres=""
        apellidos=""

        username=nombres[0:3]+apellidos[0:3]+str(datetime.datetime.now()).replace("-","").replace(" ","").replace(".","").replace(":","")
        user=User.objects.create(username=username, email=request.POST.get('email'),first_name=request.POST.get('nombres'),last_name=request.POST.get('apellidos'),
                                 is_active=True,is_staff=True)
        user.save()
        user.set_password(request.POST.get('password'))
        establecimiento=Establecimiento.objects.get(id=request.GET.get('establecimiento'))
        usuario=UsuarioEmpresa.objects.create(establecimiento=establecimiento,user=user,nombreCompleto=nombres+" "+apellidos,cedula=request.POST.get('cedula'))
        usuario.save()
    contexto={
        'usuarios':UsuarioEmpresa.objects.filter(establecimiento__usuario=request.user),
        'establecimientos':Establecimiento.objects.filter(usuario=request.user)
    }

    return render(request, 'personas/otrosUsuarios.html',contexto)

