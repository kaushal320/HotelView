from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

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


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('hotel:home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')

        # Validate password length
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return render(request, 'register.html')

        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return render(request, 'register.html')

            # Create user
            user = User.objects.create_user(
                username=email,  # Using email as username
                email=email,
                password=password
            )
            
            # Set full name
            first_name = fullname.split()[0]
            last_name = ' '.join(fullname.split()[1:]) if len(fullname.split()) > 1 else ''
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('hotel:login')

        except IntegrityError:
            messages.error(request, 'Username/Email already exists!')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('hotel:home')

def book(request):
    return render(request, 'book.html')