from django.contrib import admin
from .models import ContactSubmission, Booking, Room, RoomFeature, UserProfile

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email', 'phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'name', 'check_in', 'check_out', 'guests', 'total_price')
    list_filter = ('room_type', 'check_in')
    search_fields = ('name', 'email', 'room_type')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_guests', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('is_available', 'max_guests')

@admin.register(RoomFeature)
class RoomFeatureAdmin(admin.ModelAdmin):
    list_display = ('room', 'name', 'icon')
    search_fields = ('name', 'room__name')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__email', 'address')

admin.site.register(UserProfile, UserProfileAdmin)
