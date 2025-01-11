
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.urls import reverse
# Create your views here.

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'aboutUs.html')




def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been submitted successfully!")
            return redirect('hotel:contact')  # Replace 'contact' with the name of your contact page URL
        else:
            messages.error(request, "There was an error in your submission. Please try again.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def login(request):
    return render(request, 'login.html')


def book(request):
    return render(request, 'book.html')