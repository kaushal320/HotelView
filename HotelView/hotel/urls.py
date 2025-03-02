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
]
