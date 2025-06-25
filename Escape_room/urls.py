from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'puzzles', views.PuzzleViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'teams', views.TeamViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # Home and members area
    path('', views.home, name='home'),
    path('members/', views.members, name='members'),

    # User authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # Room views
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', views.RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),
    path('create-room/', views.create_room, name='create_room'),

    # Puzzle views
    path('puzzles/', views.puzzle_list, name='puzzle_list'),
    path('puzzles/<int:pk>/', views.puzzle_detail, name='puzzle_detail'),
    path('puzzles/create/', views.PuzzleCreateView.as_view(), name='puzzle_create'),
    path('puzzles/<int:pk>/edit/', views.PuzzleUpdateView.as_view(), name='puzzle_update'),
    path('puzzles/<int:pk>/delete/', views.PuzzleDeleteView.as_view(), name='puzzle_delete'),
    path('puzzles/<int:puzzle_id>/solve/', views.solve_puzzle, name='solve_puzzle'),
    path('puzzles/solved/', views.puzzle_solved, name='solved_puzzles'),
    path('create-puzzle/', views.create_puzzle, name='create_puzzle'),

    # Booking views
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('book-room/', views.book_room, name='book_room'),

    # Team views
    path('teams/', views.team_list, name='team_list'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('teams/create/', views.TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/edit/', views.TeamUpdateView.as_view(), name='team_update'),
    path('teams/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),
    path('teams/pick/', views.teams, name='teams'),  # For member team picking

    # Games
    path('games/', views.games, name='games'),
]
