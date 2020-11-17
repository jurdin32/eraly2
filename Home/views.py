from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "Home/login.html")


def usuario(request):
    return render(request, "Home/index2.html")