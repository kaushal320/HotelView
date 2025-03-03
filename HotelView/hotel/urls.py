from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('book/', views.book, name='book'),
    path('logout/', views.logout_view, name='logout'),
    path('booking-form/', views.booking_form, name='booking_form'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('room/<slug:room_slug>/', views.room_detail, name='room_detail'),
    path('search/', views.search_rooms, name='search'),
    path('api/search-rooms/', views.search_rooms_api, name='search_rooms_api'),
    # Booking management URLs
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
]
