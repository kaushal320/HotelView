from django.contrib import admin
from .models import ContactSubmission, Booking

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email', 'phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'name', 'check_in', 'check_out', 'guests', 'total_price')
    list_filter = ('room_type', 'check_in')
    search_fields = ('name', 'email', 'room_type')
