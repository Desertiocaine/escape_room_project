import pytest
from django.contrib.auth import get_user_model
from .models import Room, Booking
from django.utils import timezone

@pytest.mark.django_db
def test_room_str():
    room = Room.objects.create(name="Test Room", description="Desc", difficulty=1, max_players=5)
    assert str(room) == "Test Room"

@pytest.mark.django_db
def test_booking_str():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="pass")
    room = Room.objects.create(name="Test Room", description="Desc", difficulty=1, max_players=5)
    booking = Booking.objects.create(user=user, room=room, booking_time=timezone.now())
    assert user.username in str(booking)
    assert room.name in str(booking)
