from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet, PuzzleViewSet, BookingViewSet, TeamViewSet,
    room_detail, room_list, RoomCreateView, RoomUpdateView, RoomDeleteView,
    team_list, team_detail, TeamCreateView, TeamUpdateView, TeamDeleteView,
    puzzle_list, puzzle_detail, PuzzleCreateView, PuzzleUpdateView, PuzzleDeleteView,
    booking_list, booking_detail, BookingCreateView, BookingUpdateView, BookingDeleteView,
    register, solve_puzzle, home
)
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'puzzles', PuzzleViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # Room views
    path('rooms/', room_list, name='room_list'),
    path('rooms/<int:pk>/', room_detail, name='room_detail'),
    path('rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),

    # Puzzle views
    path('puzzles/', puzzle_list, name='puzzle_list'),
    path('puzzles/<int:pk>/', puzzle_detail, name='puzzle_detail'),
    path('puzzles/create/', PuzzleCreateView.as_view(), name='puzzle_create'),
    path('puzzles/<int:pk>/edit/', PuzzleUpdateView.as_view(), name='puzzle_update'),
    path('puzzles/<int:pk>/delete/', PuzzleDeleteView.as_view(), name='puzzle_delete'),
    path('puzzles/<int:puzzle_id>/solve/', solve_puzzle, name='solve_puzzle'),

    # Booking views
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/<int:pk>/', booking_detail, name='booking_detail'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),

    # Team views
    path('teams/', team_list, name='team_list'),
    path('teams/<int:pk>/', team_detail, name='team_detail'),
    path('teams/create/', TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_update'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),

    # User authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),

    # Admin and home
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]
