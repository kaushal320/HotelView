from django.core.management.base import BaseCommand
from hotel.models import Room, RoomFeature
from django.core.files.base import ContentFile
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Populate initial room data'

    def handle(self, *args, **kwargs):
        # Create rooms in the desired order
        rooms_data = [
            # First row (top)
            {
                'name': 'Double Room',
                'slug': 'double-room',
                'price': 3000,
                'max_guests': 2,
                'beds': 2,
                'size': 300,
                'rating': '★★★★☆',
                'description': 'Experience comfort and style in our Double Room. Perfect for couples or solo travelers.',
                'image': 'images/double-room.jpg',
                'features': [
                    {'name': 'Air Conditioning', 'icon': 'fas fa-snowflake'},
                    {'name': 'Room Service', 'icon': 'fas fa-concierge-bell'},
                    {'name': 'Mini Bar', 'icon': 'fas fa-glass-martini-alt'},
                ]
            },
            {
                'name': 'Luxury Room',
                'slug': 'luxury-room',
                'price': 5000,
                'max_guests': 2,
                'beds': 1,
                'size': 400,
                'rating': '★★★★★',
                'description': 'Indulge in ultimate luxury in our premium Luxury Room.',
                'image': 'images/luxury-room.jpg',
                'features': [
                    {'name': 'Jacuzzi', 'icon': 'fas fa-hot-tub'},
                    {'name': 'Room Service', 'icon': 'fas fa-concierge-bell'},
                    {'name': 'Smart TV', 'icon': 'fas fa-tv'},
                ]
            },
            {
                'name': 'Family Room',
                'slug': 'family-room',
                'price': 4000,
                'max_guests': 4,
                'beds': 2,
                'size': 500,
                'rating': '★★★★★',
                'description': 'Perfect for family stays, our Family Room offers ample space.',
                'image': 'images/family-room.jpg',
                'features': [
                    {'name': 'Kitchen', 'icon': 'fas fa-utensils'},
                    {'name': 'Play Area', 'icon': 'fas fa-gamepad'},
                    {'name': 'Multiple Beds', 'icon': 'fas fa-bed'},
                ]
            },
            # Second row (bottom)
            {
                'name': 'Small Room',
                'slug': 'small-room',
                'price': 2000,
                'max_guests': 1,
                'beds': 1,
                'size': 200,
                'rating': '★★★★☆',
                'description': 'Cozy and comfortable, perfect for solo travelers.',
                'image': 'images/small-room.jpg',
                'features': [
                    {'name': 'Work Desk', 'icon': 'fas fa-desk'},
                    {'name': 'Single Bed', 'icon': 'fas fa-bed'},
                    {'name': 'WiFi', 'icon': 'fas fa-wifi'},
                ]
            },
            {
                'name': 'Apartment',
                'slug': 'apartment',
                'price': 7000,
                'max_guests': 8,
                'beds': 3,
                'size': 800,
                'rating': '★★★★★',
                'description': 'A home away from home with full amenities.',
                'image': 'images/apartment.jpg',
                'features': [
                    {'name': 'Full Kitchen', 'icon': 'fas fa-utensils'},
                    {'name': 'Living Room', 'icon': 'fas fa-couch'},
                    {'name': 'Multiple Rooms', 'icon': 'fas fa-door-open'},
                ]
            },
            {
                'name': 'Theater Room',
                'slug': 'theater-room',
                'price': 5000,
                'max_guests': 4,
                'beds': 2,
                'size': 450,
                'rating': '★★★★★',
                'description': 'Experience cinema-quality entertainment.',
                'image': 'images/theater-room.jpg',
                'features': [
                    {'name': 'Projector', 'icon': 'fas fa-film'},
                    {'name': 'Surround Sound', 'icon': 'fas fa-volume-up'},
                    {'name': 'Reclining Seats', 'icon': 'fas fa-chair'},
                ]
            }
        ]

        # First delete existing rooms
        Room.objects.all().delete()

        # Create rooms in order
        for room_data in rooms_data:
            features = room_data.pop('features')
            image_name = room_data.pop('image').split('/')[-1]
            
            # Create room
            room = Room.objects.create(**room_data)
            
            # Copy image from static to media
            static_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', image_name)
            if os.path.exists(static_image_path):
                media_image_path = os.path.join(settings.MEDIA_ROOT, 'rooms', image_name)
                os.makedirs(os.path.dirname(media_image_path), exist_ok=True)
                shutil.copy2(static_image_path, media_image_path)
                with open(media_image_path, 'rb') as img_file:
                    room.image.save(image_name, ContentFile(img_file.read()), save=True)
            
            # Create features
            for feature in features:
                RoomFeature.objects.create(room=room, **feature)

        self.stdout.write(self.style.SUCCESS('Successfully populated rooms')) 