from django.shortcuts import render, redirect
from django.template import context
from .models import Room
from .forms import RoomForm

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

def create_room(request):
    form = RoomForm()

    if( request.method == 'POST' ):
        form = RoomForm(request.POST)
        if( form.is_valid() ):
            form.save()
            return redirect('home')

    context = { 'form': form }
    return render(request, 'base/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get( id = pk )
    form = RoomForm( instance = room )

    if( request.method == 'POST' ):
        form = RoomForm( request.POST, instance = room )
        if( form.is_valid() ):
            form.save()
            return redirect('home')

    context = { 'form': form }
    return render(request, 'base/room_form.html', context) 

def delete_room(request, pk):
    room = Room.objects.get( id = pk )
    context = { 'obj' : room }

    # Room has been actually deleted
    if( request.method == 'POST' ):
        room.delete()
        return redirect('home')
        
    return render(request, 'base/delete.html', context)