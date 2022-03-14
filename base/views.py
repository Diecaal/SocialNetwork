from urllib import request
from winreg import REG_QWORD
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.template import context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create views to be returned here


def loginPage(request):
    page = 'login'
    # No matter user writes login URL, if he is authenticated will go to home page
    if request.user.is_authenticated:
        return redirect('home')

    if(request.method == 'POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        # If everything correct, authenticate user with given data
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()

    if (request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # User data not stored yet
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured processing your form')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    # Default behaviour will return all topics
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Search room by their TOPIC name, NAME and DESCRIPTION
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count_info = f'{rooms.count()} rooms for: {q}' if q != '' else f'{rooms.count()} Rooms Open!'
    # When user search for a topic, messages feed will only be about that topic
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # Passing a dict 'rooms' to the view with our rooms list assigned
    context = {'rooms': rooms, 'topics': topics,
               'room_count_info': room_count_info,
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # Fetch all room children (messages) - order by descending order
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # When someone sends a message to the room, it will be added as a participant
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if(request.method == 'POST'):
        topic_name = request.POST.get('topic')
        # Created == True, if topic_name did not exist previously
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        room.participants.add(request.user)
        # form = RoomForm(request.POST)
        # if(form.is_valid()):
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     # First room must be created
        #     room.participants.add(request.user)
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed to do this actions')

    if(request.method == 'POST'):
        topic_name = request.POST.get('topic')
        # Created == True, if topic_name did not exist previously
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}

    if request.user != room.host:
        return HttpResponse('You are not allowed to do this actions')

    # Room has been actually deleted
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to do this actions')

    if(request.method == 'POST'):
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if(request.method == 'POST'):
        form = UserForm(request.POST, instance=user)
        if(form.is_valid()):
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'base/update-user.html', context=context)
