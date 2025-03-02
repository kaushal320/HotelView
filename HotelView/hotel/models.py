from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    guests = models.IntegerField()
    nights = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type} booking by {self.name} {self.surname}"

    class Meta:
        ordering = ['-created_at']

class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField()
    beds = models.IntegerField()
    size = models.IntegerField(help_text="Size in square feet")
    rating = models.CharField(max_length=10)
    image = models.ImageField(upload_to='rooms/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class RoomFeature(models.Model):
    room = models.ForeignKey(Room, related_name='features', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.room.name} - {self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField()

    def __str__(self):
        return f"{self.user.email}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()
