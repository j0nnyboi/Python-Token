from django.shortcuts import render

from django.http import HttpResponse

from SafeConnect import SafeToken

def index(request):
    #print(request.POST)
    return render(request, "Home.html")

def Wallet(request):
    
    return HttpResponse("Token")

