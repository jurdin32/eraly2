
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, "Home/index2.html")
    else:
        if request.POST:
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                if request.GET.get('useranon'):
                    return HttpResponseRedirect("/store/dashboard/")
                return HttpResponseRedirect("/")
            else:
                messages.add_message(request, messages.ERROR, "Lo sentimos el usuario que has ingresado no es válido, o las credenciales de ingreso fallaron..!")
                return render(request, "Home/login.html")

        else:
            return render(request, "Home/login.html")

def login_store_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/store/dashboard/")
    else:
        if request.POST:
            print(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.filter(email=request.POST.get('email')).last()

            if user is not None and user.is_active:
                user = auth.authenticate(username=user.username, password=password)
                auth.login(request, user)
                return HttpResponseRedirect("/store/dashboard/")
            else:
                messages.add_message(request, messages.ERROR, "Lo sentimos el usuario que has ingresado no es válido, o las credenciales de ingreso fallaron..!")
                return HttpResponseRedirect('/store/login/')

        else:
            return render(request, 'Store/demo-shop-8-login.html')


def logout_(request):
    logout(request)
    if request.GET.get('useranon'):
        return HttpResponseRedirect('/store/login/')
    else:
        return HttpResponseRedirect('/')