
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, PuzzleViewSet, BookingViewSet, TeamViewSet, room_detail, room_list, RoomCreateView, \
    RoomUpdateView, RoomDeleteView, team_list, team_detail, TeamCreateView, TeamUpdateView, TeamDeleteView, register
from django.contrib.auth import views as auth_views

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
    path('teams/', team_list, name='team_list'),
    path('teams/<int:pk>/', team_detail, name='team_detail'),
    path('teams/create/', TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_update'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register', register, name='register'),
]
