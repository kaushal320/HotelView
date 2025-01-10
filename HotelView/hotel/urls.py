from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('book/', views.book, name='book'),
]
