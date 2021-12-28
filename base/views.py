from django.shortcuts import render

# Create views to be returned here

rooms = [
    {'id': 1, 'name': 'First room'},
    {'id': 2, 'name': 'Second room'},
    {'id': 3, 'name': 'Third room'},
]

def home(request):
    # Passing a dict 'rooms' to the view with our rooms list assigned
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = None
    for currentRoom in rooms:
        if currentRoom['id'] == int(pk):
            room = currentRoom
    context = {'room': room}
    return render(request, 'base/room.html', context)