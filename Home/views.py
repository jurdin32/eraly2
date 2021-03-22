
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

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
                return HttpResponseRedirect("/")
            else:
                return render(request, "Home/login.html")
        else:
            return render(request, "Home/login.html")

def logout_(request):
    logout(request)
    return render(request, "Home/login.html")