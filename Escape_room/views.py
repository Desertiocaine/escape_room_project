# --- Standard Library Imports ---
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# --- Django Auth Imports ---
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test

# --- Django Generic Views ---
from django.views.generic import CreateView, UpdateView, DeleteView

# --- DRF Imports ---
from rest_framework import viewsets

# --- Local App Imports ---
from .models import Room, Puzzle, Booking, Team
from .serializers import RoomSerializer, PuzzleSerializer, BookingSerializer, TeamSerializer

# ===========================
# BASIC FUNCTION-BASED VIEWS
# ===========================

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('team_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# ===========================
# ROOM VIEWS
# ===========================

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    puzzles = room.puzzles.all()
    return render(request, 'room_detail.html', {'room': room, 'puzzles': puzzles})

class RoomCreateView(CreateView):
    model = Room
    fields = ['name', 'description', 'difficulty', 'max_players']
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')

class RoomUpdateView(UpdateView):
    model = Room
    fields = ['name', 'description', 'difficulty', 'max_players']
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

# ===========================
# PUZZLE VIEWS
# ===========================

def puzzle_list(request):
    puzzles = Puzzle.objects.all()
    return render(request, 'puzzle_list.html', {'puzzles': puzzles})

def puzzle_detail(request, pk):
    puzzle = get_object_or_404(Puzzle, pk=pk)
    return render(request, 'puzzle_detail.html', {'puzzle': puzzle})

def solve_puzzle(request, puzzle_id):
    puzzle = get_object_or_404(Puzzle, id=puzzle_id)
    if request.method == "POST":
        user_answer = request.POST.get("answer", "").strip()
        if user_answer.lower() == puzzle.answer.lower():
            return render(request, "puzzle_solved.html", {"puzzle": puzzle, "correct": True})
        else:
            return render(request, "puzzle_solved.html", {"puzzle": puzzle, "correct": False})
    return HttpResponseRedirect(reverse("room_detail", args=[puzzle.room.id]))

class PuzzleCreateView(CreateView):
    model = Puzzle
    fields = ['name', 'description', 'answer', 'room']
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_list')

class PuzzleUpdateView(UpdateView):
    model = Puzzle
    fields = ['name', 'description', 'answer', 'room']
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_list')

class PuzzleDeleteView(DeleteView):
    model = Puzzle
    template_name = 'puzzle_confirm_delete.html'
    success_url = reverse_lazy('puzzle_list')

# ===========================
# BOOKING VIEWS
# ===========================

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_detail.html', {'booking': booking})

class BookingCreateView(CreateView):
    model = Booking
    fields = ['user', 'room', 'booking_time']
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingUpdateView(UpdateView):
    model = Booking
    fields = ['user', 'room', 'booking_time']
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')

# ===========================
# TEAM VIEWS
# ===========================

@user_passes_test(lambda u: u.is_staff)
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'team_list.html', {'teams': teams})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = team.members.all()
    return render(request, 'team_detail.html', {'team': team, 'members': members})

class TeamCreateView(UserPassesTestMixin, CreateView):
    model = Team
    fields = ['name', 'members', 'room']
    template_name = 'team_form.html'
    success_url = reverse_lazy('team_list')
    def test_func(self):
        return self.request.user.is_staff

class TeamUpdateView(UserPassesTestMixin, UpdateView):
    model = Team
    fields = ['name', 'members', 'room']
    template_name = 'team_form.html'
    success_url = reverse_lazy('team_list')
    def test_func(self):
        return self.request.user.is_staff

class TeamDeleteView(UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'team_confirm_delete.html'
    success_url = reverse_lazy('team_list')
    def test_func(self):
        return self.request.user.is_staff

# ===========================
# DRF VIEWSETS
# ===========================

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
