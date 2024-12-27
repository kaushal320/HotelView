from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')


def about(request):
    return render(request,'aboutUs.html')


def contact(request):
    return render(request,'contact.html')


def booking(request):
    return render(request,'booking.html')


def login(request):
    return render(request,'login.html')