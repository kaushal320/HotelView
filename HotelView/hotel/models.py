from django.db import models
from django.contrib.auth.models import User

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
