from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    #print(request.POST)
    return render(request, "Home.html")

def Token(request):
    return HttpResponse("Token")

def images(request):
    return render(request, "images/SafeCoin_Icon.png")
