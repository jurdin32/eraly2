
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from Empresa.models import Establecimiento, UsuarioEmpresa
from Producto.models import Categorias


def index(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active and user.is_staff:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.add_message(request, messages.ERROR, "Lo sentimos el usuario que has ingresado no es válido, o las credenciales de ingreso fallaron..!")
            return render(request, "Home/login.html")
    if request.session.get('tiendas_usuario'):
        del request.session['tiendas_usuario']

    if request.user.is_authenticated and request.user.is_staff:
        ti=[]
        for tiendas in UsuarioEmpresa.objects.filter(user=request.user):
            ti.append({'slug':tiendas.establecimiento.slug, 'nombre':tiendas.establecimiento.slug})
        request.session['tiendas_usuario']=ti
        return render(request, "Home/index2.html")
    else:
        return HttpResponseRedirect("/store/")



def login_store_user(request):
    contexo={
        'categorias':Categorias.objects.all()
    }
    if request.user.is_authenticated:
        return HttpResponseRedirect("/store/dashboard/")
    else:
        if request.POST:
            print(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.filter(email=request.POST.get('email')).last()
            if user is not None and user.is_active:
                try:
                    user = auth.authenticate(username=user.username, password=password)
                    auth.login(request, user)
                    return HttpResponseRedirect("/store/dashboard/")
                except Exception as error:
                    messages.add_message(request, messages.ERROR, "Lo sentimos el usuario que has ingresado no es válido, o las credenciales de ingreso fallaron..!")
                    return HttpResponseRedirect('/store/login/')
            else:
                messages.add_message(request, messages.ERROR, "Lo sentimos el usuario que has ingresado no es válido, o las credenciales de ingreso fallaron..!")
                return HttpResponseRedirect('/store/login/')
    return render(request, 'Store/demo-shop-8-login.html',contexo)


def logout_(request):
    logout(request)
    if request.GET.get('useranon'):
        return HttpResponseRedirect('/store/login/')
    else:
        return HttpResponseRedirect('/')

def politica(request):

    return HttpResponse("Politica de Uso")