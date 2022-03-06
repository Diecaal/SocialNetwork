from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    '''
    A topic which will be assigned to one or more rooms
    '''
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    '''
    Room class that will hold messages about a specific topic
    '''
    # id = we can add the usage as UID for example
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # if we use SET_NULL approach, specificy that database can contain null for that value
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # allow empty field
    # participants =
    # takes timestamp when is called/update [>= ONCE]
    updated = models.DateTimeField(auto_now=True)
    # takes a timestamp when method is created [ONCE]
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        # (-) Reverse ordering -> most updated Rooms will be showed first

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    '''
    Message created by a user assigned to a room
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # When parent (room) all children (messages) will be deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body[0:50])  # First 50 characters of the messsage
