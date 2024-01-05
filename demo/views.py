# Create your views here.
from django.shortcuts import render


#Create your views here.


def display(request):
    # return HttpResponse("Welcome to Django")  # you need an end point to connect to this function.
    return render(request, 'demo/hello.html', {"name": "Dee"})
