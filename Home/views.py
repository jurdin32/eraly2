from django.shortcuts import render

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, "Home/index2.html")
    else:
        return render(request, "Home/login.html")