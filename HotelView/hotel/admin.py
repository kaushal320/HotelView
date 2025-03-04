from django.contrib import admin
from .models import ContactSubmission, Booking, Room, RoomFeature, UserProfile

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email', 'phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'user', 'check_in', 'check_out', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'room_type', 'check_in')
    search_fields = ('user__username', 'user__email', 'room_type', 'name', 'surname')
    actions = ['confirm_bookings', 'reject_bookings']
    
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_bookings.short_description = "Confirm selected bookings"
    
    def reject_bookings(self, request, queryset):
        queryset.update(status='rejected')
    reject_bookings.short_description = "Reject selected bookings"

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
