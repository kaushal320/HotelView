from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static



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
            return redirect('hotel:contact')  
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
            messages.success(request, f'Welcome, {user.first_name}!')
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
    page = request.GET.get('page')
    return render(request, 'book.html', {'page': page})

def booking_form(request):
    room_type = request.GET.get('room_type')
    
    # Define room configurations including price, max guests, image and rating
    room_configs = {
        'Theater Room': {
            'price': 500,
            'max_guests': 2,
            'image': 'images/theater-room.jpg',
            'rating': '★★★★★'
        },
        'Apartment': {
            'price': 5000,
            'max_guests': 6,
            'image': 'images/apartment.jpg',
            'rating': '★★★★★'
        },
        'Family Room': {
            'price': 4000,
            'max_guests': 4,
            'image': 'images/family-room.jpg',
            'rating': '★★★★★'
        },
        'Double Room': {
            'price': 3000,
            'max_guests': 2,
            'image': 'images/double-room.jpg',
            'rating': '★★★★☆'
        },
        'Small Room': {
            'price': 2000,
            'max_guests': 1,
            'image': 'images/small-room.jpg',
            'rating': '★★★★☆'
        },
        'Luxury Room': {
            'price': 5000,
            'max_guests': 2,
            'image': 'images/luxury-room.jpg',
            'rating': '★★★★★'
        }
    }

    # Get room configuration or use default values
    room_config = room_configs.get(room_type, {
        'price': 4000,
        'max_guests': 2,
        'image': 'images/default-room.jpg',
        'rating': '★★★★☆'
    })

    context = {
        'room_type': room_type,
        'room_price': room_config['price'],
        'max_guests': room_config['max_guests'],
        'room_image': room_config['image'],
        'room_rating': room_config['rating'],
        'check_in_day': '16',
        'check_in_month': 'Dec, 2024',
        'check_in_weekday': 'TUESDAY',
        'check_out_day': '16',
        'check_out_month': 'Dec, 2024',
        'check_out_weekday': 'TUESDAY',
    }
    
    return render(request, 'booking_form.html', context)