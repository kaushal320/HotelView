
from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.index,name='index'),
    path("", views.about,name='about'),
    path("", views.contact,name='contact'),
     
]
