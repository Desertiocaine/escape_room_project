python
from rest_framework import viewsets
from .models import Room, Puzzle, Booking, Team
from .serializers import RoomSerializer, PuzzleSerializer, BookingSerializer, TeamSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class PuzzleViewSet(viewsets.ModelViewSet):
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

# Create your views here.
