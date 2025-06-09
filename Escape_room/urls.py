python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, PuzzleViewSet, BookingViewSet, TeamViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'puzzles', PuzzleViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
