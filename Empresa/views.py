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