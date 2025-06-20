from django.db import models
from django.conf import settings

class Room(models.Model):
    """Represents an escape room with its details."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.IntegerField()
    max_players = models.IntegerField()

    def __str__(self):
        return self.name



class Puzzle(models.Model):
    """Represents a puzzle that is linked to a room"""
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='puzzles')
    question = models.TextField()
    answer = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return f"Puzzle {self.order} for {self.room.name}"


class Booking(models.Model):
    """Represents a booking for an escape room."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    booking_time = models.DateTimeField()
    team_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.name} at {self.booking_time}"



class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

