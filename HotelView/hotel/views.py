from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactForm
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from .models import Booking, Room, RoomFeature, UserProfile
from datetime import datetime, timedelta, date



def home(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'index.html', {'rooms': rooms})


def about(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'aboutUs.html', {'rooms': rooms})




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
            
            # Get the next URL from POST data (more secure than GET)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('hotel:home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    next_url = request.GET.get('next', '')
    return render(request, 'login.html', {'next': next_url})

def register(request):
    if request.method == 'POST':
        try:
            # Check if passwords match
            if request.POST['password1'] != request.POST['password2']:
                messages.error(request, 'Passwords do not match')
                return render(request, 'register.html')

            # Get form data
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            password = request.POST['password1']

            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create or update profile
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'address': address}
            )

            messages.success(request, 'Registration successful! Please login.')
            return redirect('hotel:login')

        except IntegrityError:
            messages.error(request, 'This email is already registered')
        except Exception as e:
            messages.error(request, f'Registration error: {str(e)}')

    return render(request, 'register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('hotel:home')

def book(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'book.html', {'rooms': rooms})

@login_required(login_url='hotel:login')
def booking_form(request):
    room_type = request.GET.get('room_type')
    try:
        room = Room.objects.get(name=room_type)
        room_features = room.features.all()  # Get all features for this room
    except Room.DoesNotExist:
        messages.error(request, 'Room not found')
        return redirect('hotel:book')

    context = {
        'room': room,  # Pass the entire room object
        'room_type': room.name,
        'room_price': room.price,
        'max_guests': room.max_guests,
        'room_rating': room.rating,
        'room_features': room_features,  # Pass the features
        'today': date.today(),
        'user': request.user,
    }
    
    if request.method == 'POST':
        # Get form data
        guests = int(request.POST.get('guests'))
        nights = int(request.POST.get('nights'))
        total_price = request.POST.get('total_price')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        arrival = request.POST.get('arrival')

        # Convert arrival string to datetime
        check_in = datetime.strptime(arrival, '%Y-%m-%d')
        check_out = check_in + timedelta(days=nights)

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            room_type=room.name,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            nights=nights,
            total_price=total_price,
            name=name,
            surname=surname,
            email=email,
            address=address
        )

        messages.success(request, 'Booking completed successfully!')
        return redirect('hotel:booking_confirmation', booking_id=booking.id)
    
    return render(request, 'booking_form.html', context)

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_confirmation.html', {'booking': booking})

def room_detail(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    similar_rooms = Room.objects.exclude(id=room.id)[:3]
    
    context = {
        'room': room,
        'similar_rooms': similar_rooms
    }
    return render(request, 'room_detail.html', context)