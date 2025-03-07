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
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.utils import timezone



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
        room_features = room.features.all()
        
        # Get count of bookings for this room type by the current user
        same_room_bookings = Booking.objects.filter(
            user=request.user,
            room=room
        ).count()
        
    except Room.DoesNotExist:
        messages.error(request, 'Room not found')
        return redirect('hotel:book')

    context = {
        'room': room,
        'room_type': room.name,
        'room_price': room.price,
        'max_guests': room.max_guests,
        'room_rating': room.rating,
        'room_features': room_features,
        'today': timezone.now().date(),
        'user': request.user,
        'same_room_bookings': same_room_bookings,
    }
    
    if request.method == 'POST':
        try:
            # Check if user has already booked this room type 3 times
            if same_room_bookings >= 3:
                messages.error(request, f'You have already booked {room.name} 3 times. Please choose a different room type.')
                return render(request, 'booking_form.html', context)
            
            # Get form data
            arrival = request.POST.get('arrival')
            if not arrival:
                messages.error(request, 'Please select a check-in date')
                return render(request, 'booking_form.html', context)

            guests = request.POST.get('guests')
            if not guests:
                messages.error(request, 'Please specify the number of guests')
                return render(request, 'booking_form.html', context)

            nights = request.POST.get('nights')
            if not nights:
                messages.error(request, 'Please specify the number of nights')
                return render(request, 'booking_form.html', context)

            name = request.POST.get('name')
            if not name:
                messages.error(request, 'Please enter your first name')
                return render(request, 'booking_form.html', context)

            surname = request.POST.get('surname')
            if not surname:
                messages.error(request, 'Please enter your last name')
                return render(request, 'booking_form.html', context)

            email = request.POST.get('email')
            if not email:
                messages.error(request, 'Please enter your email address')
                return render(request, 'booking_form.html', context)

            address = request.POST.get('address')
            if not address:
                messages.error(request, 'Please enter your address')
                return render(request, 'booking_form.html', context)

            # Convert values to appropriate types
            guests = int(guests)
            nights = int(nights)

            # Convert arrival string to datetime with timezone
            check_in = timezone.make_aware(datetime.strptime(arrival, '%Y-%m-%d'))
            # Add current time to check_in
            current_time = timezone.now().time()
            check_in = timezone.make_aware(datetime.combine(check_in.date(), current_time))
            
            # Set checkout time to 12:00 PM (noon)
            check_out_date = check_in.date() + timedelta(days=nights)
            check_out = timezone.make_aware(datetime.combine(check_out_date, datetime.strptime('12:00', '%H:%M').time()))

            # Validate dates
            if check_in.date() < timezone.now().date():
                messages.error(request, 'Check-in date cannot be in the past')
                return render(request, 'booking_form.html', context)

            # Calculate total price: base price + 500 for each additional night
            total_price = room.price + (nights - 1) * 500

            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                room=room,
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

            messages.success(request, 'Booking completed successfully! Your booking is pending admin confirmation.')
            return redirect('hotel:booking_confirmation', booking_id=booking.id)

        except ValueError as e:
            messages.error(request, f'Invalid input: {str(e)}')
            return render(request, 'booking_form.html', context)
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'booking_form.html', context)
    
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

def search_rooms(request):
    query = request.GET.get('q', '')
    if query:
        rooms = Room.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).filter(is_available=True)
    else:
        rooms = Room.objects.filter(is_available=True)
    
    context = {
        'rooms': rooms,
        'query': query
    }
    return render(request, 'search_results.html', context)

def search_rooms_api(request):
    query = request.GET.get('q', '')
    if query:
        rooms = Room.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).filter(is_available=True)[:5]  # Limit to 5 results
        
        results = [{
            'name': room.name,
            'slug': room.slug,
            'price': str(room.price),
            'max_guests': room.max_guests,
            'image': room.image.url,
        } for room in rooms]
        
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room').order_by('-created_at')
    today = date.today()
    return render(request, 'user_bookings.html', {'bookings': bookings, 'today': today})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Get form data
            arrival = request.POST.get('arrival')
            if not arrival:
                messages.error(request, 'Please select a check-in date')
                return redirect('hotel:edit_booking', booking_id=booking_id)

            guests = request.POST.get('guests')
            if not guests:
                messages.error(request, 'Please specify the number of guests')
                return redirect('hotel:edit_booking', booking_id=booking_id)

            nights = request.POST.get('nights')
            if not nights:
                messages.error(request, 'Please specify the number of nights')
                return redirect('hotel:edit_booking', booking_id=booking_id)

            # Convert values to appropriate types
            guests = int(guests)
            nights = int(nights)

            # Convert arrival string to datetime with timezone
            check_in = timezone.make_aware(datetime.strptime(arrival, '%Y-%m-%d'))
            # Keep the original check-in time
            check_in = timezone.make_aware(datetime.combine(check_in.date(), booking.check_in.time()))
            
            # Set checkout time to 12:00 PM (noon)
            check_out_date = check_in.date() + timedelta(days=nights)
            check_out = timezone.make_aware(datetime.combine(check_out_date, datetime.strptime('12:00', '%H:%M').time()))

            # Validate dates
            if check_in.date() < timezone.now().date():
                messages.error(request, 'Check-in date cannot be in the past')
                return redirect('hotel:edit_booking', booking_id=booking_id)

            # Calculate total price: base price + 500 for each additional night
            total_price = booking.room.price + (nights - 1) * 500

            # Update booking
            booking.check_in = check_in
            booking.check_out = check_out
            booking.guests = guests
            booking.nights = nights
            booking.total_price = total_price
            booking.status = 'pending'  # Reset status to pending after edit
            booking.save()

            messages.success(request, 'Booking updated successfully! Your booking is pending admin confirmation.')
            return redirect('hotel:booking_detail', booking_id=booking.id)

        except ValueError as e:
            messages.error(request, f'Invalid input: {str(e)}')
            return redirect('hotel:edit_booking', booking_id=booking_id)
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('hotel:edit_booking', booking_id=booking_id)

    context = {
        'booking': booking,
        'room': booking.room,
        'today': timezone.now().date(),
    }
    return render(request, 'edit_booking.html', context)

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('hotel:user_bookings')
    
    return render(request, 'delete_booking.html', {'booking': booking})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    today = date.today()
    return render(request, 'booking_detail.html', {'booking': booking, 'today': today})