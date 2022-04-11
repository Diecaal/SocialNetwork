from django.contrib import admin
from .models import Room, Topic, Message, User  # Import models classes from models.py

# Register your models here.

admin.site.register(User)
admin.site.register(Room)  # Adds a new group under "Rooms" under Base, in Django Admin page
admin.site.register(Topic)
admin.site.register(Message)
