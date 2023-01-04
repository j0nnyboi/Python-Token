from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    print(request.POST)
    return render(request, "training/training.html", {'Answer': my_answer})
    
    return HttpResponse("Hello, world. You're at the polls index.")
def Token(request):
    return HttpResponse("Token")
