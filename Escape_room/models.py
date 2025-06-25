from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

class Room(models.Model):
    """Represents an escape room with its details."""

    DIFFICULTY_CHOICES = [
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="No description provided.")
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    max_players = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], default=6)

    def __str__(self):
        return f"{self.name} ({self.get_difficulty_display()}) - Up to {self.max_players} players"

class Puzzle(models.Model):
    """Represents a puzzle within an escape room."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='puzzles')
    name = models.CharField(max_length=100)
    description = models.TextField()
    question = models.TextField(default="")
    solution = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Room: {self.room.name})"

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    """Represents a booking for a team in a room."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField(default=60)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team.name} booked {self.room.name} at {self.booking_time}"

