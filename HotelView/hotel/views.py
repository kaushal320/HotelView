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
from .models import Booking
from datetime import datetime, timedelta



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

@login_required
def booking_form(request):
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
        room_type = request.GET.get('room_type')

        # Convert arrival string to datetime
        check_in = datetime.strptime(arrival, '%Y-%m-%dT%H:%M')
        check_out = check_in + timedelta(days=nights)

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            room_type=room_type,
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

    # Your existing GET logic here
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

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_confirmation.html', {'booking': booking})

def room_detail(request, room_slug):
    # Room configurations with detailed information
    room_configs = {
        'double-room': {
            'name': 'Double Room',
            'image': 'images/double-room.jpg',
            'additional_images': [
                'images/double-room.jpg',
                'images/double-room.jpg',
                'images/double-room.jpg'
            ],
            'price': 3000,
            'rating': '★★★★☆',
            'beds': 2,
            'max_guests': 2,
            'size': 300,
            'description': 'The Double Room is a cozy 25 ft² accommodation designed to comfortably host up to two guests, making it an ideal choice for couples or solo travelers. Priced at Rs 3000 per night, this room offers the perfect blend of affordability and comfort. It features modern amenities, stylish furnishings, and a peaceful ambiance to ensure a relaxing and enjoyable stay. ',
            'features': [
                {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
                {'name': 'Room Service', 'icon': 'fas fa-concierge-bell'},
            ],
            'slug': 'double-room'
        },
        'luxury-room': {
            'name': 'Luxury Room',
            'image': 'images/luxury-room.jpg',
            'additional_images': [
                'images/luxury-room.jpg',
                'images/luxury-room.jpg',
                'images/luxury-room.jpg'
            ],
            'price': 5000,
            'rating': '★★★★★',
            'beds': 1,
            'max_guests': 2,
            'size': 400,
            'description': 'The Luxury Room is an elegant 20 ft² accommodation designed to host up to two guests, offering a perfect blend of sophistication and comfort. Priced at Rs 5000 per night, this room is ideal for travelers seeking a premium experience.Featuring high-end furnishings, modern amenities, and a serene ambiance, the Luxury Room provides an exceptional setting for relaxation and indulgence.',
            'features': [
                {'name': 'Luxury Bathroom', 'icon': 'fas fa-hot-tub'},
                {'name': 'Room Service', 'icon': 'fas fa-concierge-bell'},
                {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
            ],
            
            'slug': 'luxury-room'
        },
        'family-room': {
            'name': 'Family Room',
            'image': 'images/family-room.jpg',
            'additional_images': [
                'images/family-room.jpg',
                'images/family-room.jpg',
                'images/family-room.jpg'
            ],
            'price': 4000,
            'rating': '★★★★★',
            'beds': 4,
            'max_guests': 4,
            'size': 500,
            'description': 'The Family Room is a spacious 30 ft² accommodation designed to comfortably host up to four guests, making it an ideal choice for families or small groups. Priced at Rs.4,000 per night, the room combines comfort, style, and affordability. Guests staying for an extended period can enjoy a special discounted weekly rate, perfect for longer vacations or business stays.',
            'features': [
                {'name': 'Family Space', 'icon': 'fas fa-users'},
                {'name': 'Kids Corner', 'icon': 'fas fa-baby'},
                {'name': 'Entertainment', 'icon': 'fas fa-tv'},
                {'name': 'Room Service', 'icon': 'fas fa-concierge-bell'},
                {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
            ],
            'slug': 'family-room'
        },
        'small-room': {
            'name': 'Small Room',
            'image': 'images/small-room.jpg',
            'additional_images': [
                'images/small-room.jpg',
                'images/small-room.jpg',
                'images/small-room.jpg'
            ],
            'price': 2000,
            'rating': '★★★★☆',
            'beds': 1,
            'max_guests': 1,
            'description': 'The Small Room is a compact and cozy 15 ft² accommodation designed for one guest, offering comfort and convenience at an affordable price. Priced at Rs 2000 per night, this room is perfect for solo travelers, students, or business guests seeking a budget-friendly option. Despite its size, the room features essential amenities, comfortable furnishings, and a peaceful atmosphere to ensure a pleasant stay..',
            'features': [
                {'name': 'Single Bed', 'icon': 'fas fa-bed'},
                {'name': 'Room Service', 'icon': 'fas fa-concierge-bell'},
                {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
            ],
            'slug': 'small-room'
        },
        'apartment': {
            'name': 'Apartment',
            'image': 'images/apartment.jpg',
            'additional_images': [
                'images/apartment.jpg',
                'images/apartment.jpg',
                'images/apartment.jpg'
            ],
            'price': 7000,
            'rating': '★★★★★',
            'beds': 4,
            'max_guests': 8,
            'size': 800,
            'description': 'The Apartment is a spacious 70 ft² accommodation, perfect for those seeking a home-like experience during their stay. Priced at Rs 7000 per night, this apartment offers ample space, ideal for families, small groups, or extended stays. It features modern furnishings, a fully equipped kitchenette, and all the amenities needed for comfort and convenience. Whether you are on a business trip, vacation, or looking for a longer stay, the Apartment provides a cozy, private retreat with everything you need for a memorable and relaxing experience.',
            'features': [
                {'name': 'Full Kitchen', 'icon': 'fas fa-utensils'},
                {'name': 'Living Room', 'icon': 'fas fa-couch'},
                {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
            ],
            'slug': 'apartment'
        },
        'theater-room': {
            'name': 'Theater Room',
            'image': 'images/theater-room.jpg',
            'additional_images': [
                'images/theater-room.jpg',
                'images/theater-room.jpg',
                'images/theater-room.jpg'
            ],
            'price': 500,
            'rating': '★★★★★',
            'beds': 4,
            'max_guests': 4,
            'size': 350,
            'description': 'The Theater Room is a luxurious 70 ft² space, designed to provide an immersive cinematic experience. Priced at Rs 5000 per night, this room is perfect for movie enthusiasts, families, or groups who want to enjoy a private theater experience. It is equipped with high-quality sound systems, a large screen, and comfortable seating, ensuring a premium viewing experience. Whether you are hosting a movie night, enjoying your favorite shows, or having a special event, the Theater Room offers an exceptional setting for entertainment and relaxation. With its modern amenities and cozy atmosphere, its the perfect retreat for a memorable cinematic experience.',
            'features': [
                {'name': 'Projector Screen', 'icon': 'fas fa-film'},
                {'name': 'Surround Sound', 'icon': 'fas fa-volume-up'},
                {'name': 'Movie Library', 'icon': 'fas fa-server'},
                {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
                {'name': 'Food Service', 'icon': 'fas fa-concierge-bell'}
            ],
            'slug': 'theater-room'
        }
    }

    room = room_configs.get(room_slug)
    if not room:
        return redirect('hotel:home')

    # Get similar rooms (excluding current room)
    similar_rooms = [r for slug, r in room_configs.items() if slug != room_slug][:3]

    context = {
        'room': room,
        'similar_rooms': similar_rooms
    }
    return render(request, 'room_detail.html', context)