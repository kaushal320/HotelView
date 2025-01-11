from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'aboutUs.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    return render(request, 'login.html')


def book(request):
    return render(request, 'book.html')