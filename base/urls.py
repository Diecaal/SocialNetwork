from django.urls import path
from . import views

urlpatterns = [
    # Going to views.py and select view given by def home()
    path('', views.home, name='home'), 
    path('room/<str:pk>/', views.room, name='room'),
]