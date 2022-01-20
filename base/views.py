from django.shortcuts import render
from .models import Room

# Create views to be returned here

def home(request):
    rooms = Room.objects.all()
    # Passing a dict 'rooms' to the view with our rooms list assigned
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)