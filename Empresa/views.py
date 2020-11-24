from django.shortcuts import render

# Create your views here.
def empresa(request):
    contexto={

    }
    return render(request, "empresa/empresa.html", contexto)

def registroEmpresa(request):
    contexto={

    }
    return render(request,'empresa/empresa.html',contexto)