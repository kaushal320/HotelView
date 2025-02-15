from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('book/', views.book, name='book'),
    path('logout/', views.logout_view, name='logout'),
    path('booking-form/', views.booking_form, name='booking_form'),
]
