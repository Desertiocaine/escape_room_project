from django.contrib.auth import get_user_model
from .models import Room, Booking
from django.utils import timezone
from django.test import TestCase

class RoomModelTest(TestCase):
    def test_room_str(self):
        room = Room.objects.create(name="Test Room", description="Desc", difficulty=1, max_players=5)
        self.assertEqual(str(room), "Test Room")

class BookingModelTest(TestCase):
    def test_booking_str(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="pass")
        room = Room.objects.create(name="Test Room", description="Desc", difficulty=1, max_players=5)
        booking = Booking.objects.create(user=user, room=room, booking_time=timezone.now())
        self.assertIn(user.username, str(booking))
        self.assertIn(room.name, str(booking))
