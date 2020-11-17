
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

def index(request):
    if request.user.is_authenticated:

        return render(request, "Home/index2.html")
    else:
        return render(request, "Home/login.html")

def logout_(request):
    logout(request)
    return render(request, "Home/login.html")