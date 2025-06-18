python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, PuzzleViewSet, BookingViewSet, TeamViewSet, room_detail, room_list, RoomCreateView, RoomUpdateView, RoomDeleteView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'puzzles', PuzzleViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('rooms/', room_list, name='room_list'),
    path('rooms/<int:pk>/', room_detail, name='room_detail'),
    path('rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('admin/', admin.site.urls),
]
