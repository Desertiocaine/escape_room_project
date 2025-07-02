# --- Standard Library Imports ---
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse

# --- Django Auth Imports ---
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# --- Django Generic Views ---
from django.views.generic import CreateView, UpdateView, DeleteView

# --- DRF Imports ---
from rest_framework import viewsets

# --- Local App Imports ---
from .models import Room, Puzzle, Booking, Team, RoomProgress
from .serializers import RoomSerializer, PuzzleSerializer, BookingSerializer, TeamSerializer

# ===========================
# BASIC FUNCTION-BASED VIEWS
# ===========================

def home(request):
    return render(request, 'home.html')

@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams})

@login_required
def book_room(request):
    return render(request, 'book_room.html')

@login_required
def games(request):
    return render(request, 'games.html')

@user_passes_test(lambda u: u.is_staff)
def create_room(request):
    return render(request, 'create_room.html')

@user_passes_test(lambda u: u.is_staff)
def create_puzzle(request):
    return render(request, 'create_puzzle.html')

@login_required
def members(request):
    return render(request, 'members.html')

@login_required
def join_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.members.add(request.user)
    team.save()
    messages.success(request, f"You joined the team: {team.name}")
    return redirect('team_list')

@login_required
def restart_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    progress_qs = RoomProgress.objects.filter(user=request.user, room=room)
    print("Before delete:", progress_qs.exists())
    progress_qs.delete()
    print("After delete:", RoomProgress.objects.filter(user=request.user, room=room).exists())
    return redirect('room_detail', room_id=room_id)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('members')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# ===========================
# ROOM VIEWS
# ===========================

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    # Get the next unsolved puzzle for this room
    next_puzzle = Puzzle.objects.filter(room=room, solved=False).order_by('order').first()
    background_images = room.background_images()
    puzzle_order = next_puzzle.order if next_puzzle else 1

    if request.method == 'POST' and next_puzzle:
        answer = request.POST.get('answer', '').strip().lower()
        if answer == next_puzzle.answer.strip().lower():
            next_puzzle.solved = True
            next_puzzle.save()
            # Reload the next unsolved puzzle
            return redirect('room_detail', room_id=room.id)
        else:
             messages.error(request, "Incorrect answer. Try again.")

    return render(request, 'room_detail.html', {
        'room': room,
        'puzzle': next_puzzle,
        'background_images': background_images,
        'puzzle_order': puzzle_order,
    })

class RoomCreateView(UserPassesTestMixin, CreateView):
    model = Room
    fields = ['name', 'description', 'max_players']
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')
    def test_func(self):
        return self.request.user.is_staff

class RoomUpdateView(UserPassesTestMixin, UpdateView):
    model = Room
    fields = ['name', 'description', 'max_players']
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')
    def test_func(self):
        return self.request.user.is_staff

class RoomDeleteView(UserPassesTestMixin, DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')
    def test_func(self):
        return self.request.user.is_staff

# ===========================
# PUZZLE VIEWS
# ===========================

def puzzle_list(request):
    puzzles = Puzzle.objects.all()
    return render(request, 'puzzle_list.html', {'puzzles': puzzles})

def puzzle_detail(request, room_id, puzzle_id):
    room = get_object_or_404(Room, pk=room_id)
    puzzle = get_object_or_404(Puzzle, pk=puzzle_id, room=room)
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        answer = request.POST.get('answer', '').strip()
        correct = (answer.lower() == puzzle.solution.lower())
        if correct:
            # Get next puzzle or set finished
            next_puzzle = ... # your logic here
            if next_puzzle:
                return JsonResponse({
                    'correct': True,
                    'next_question': next_puzzle.question,
                    'next_description': next_puzzle.description,
                    'next_name': next_puzzle.name,
                    'next_order': next_puzzle.order,
                })
            else:
                return JsonResponse({'correct': True, 'finished': True})
        else:
            return JsonResponse({'correct': False})

def solve_puzzle(request, puzzle_id):
    puzzle = get_object_or_404(Puzzle, pk=puzzle_id)
    if request.method == 'POST':
        user_answer = request.POST.get('answer', '').strip().lower()
        correct_answer = puzzle.answer.strip().lower()
        if user_answer == correct_answer:
            puzzle.solved = True
            puzzle.save()
            next_puzzle = Puzzle.objects.filter(
                room=puzzle.room,
                id__gt=puzzle.id
            ).order_by('id').first()
            if next_puzzle:
                messages.success(request, "Correct! Moving to the next puzzle.")
                return redirect('solve_puzzle', puzzle_id=next_puzzle.pk)
            else:
                messages.success(request, "You've completed all puzzles!")
                return redirect('puzzle_solved')
        else:
            messages.error(request, "Incorrect answer. Try again.")
    return render(request, 'solve_puzzle.html', {'puzzle': puzzle})

def puzzle_solved(request):
    return render(request, 'puzzle_solved.html')

class PuzzleCreateView(UserPassesTestMixin, CreateView):
    model = Puzzle
    fields = ['name', 'description', 'answer', 'room']
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_list')
    def test_func(self):
        return self.request.user.is_staff

class PuzzleUpdateView(UserPassesTestMixin, UpdateView):
    model = Puzzle
    fields = ['name', 'description', 'answer', 'room']
    template_name = 'puzzle_form.html'
    success_url = reverse_lazy('puzzle_list')
    def test_func(self):
        return self.request.user.is_staff

class PuzzleDeleteView(UserPassesTestMixin, DeleteView):
    model = Puzzle
    template_name = 'puzzle_confirm_delete.html'
    success_url = reverse_lazy('puzzle_list')
    def test_func(self):
        return self.request.user.is_staff

# ===========================
# BOOKING VIEWS
# ===========================

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_detail.html', {'booking': booking})

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['team', 'room', 'duration_minutes']
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = ['room', 'team', 'duration_minutes']
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')

# ===========================
# TEAM VIEWS
# ===========================

def team_list_view(request):
    teams = Team.objects.all()
    return render(request, 'team_list.html', {'teams': teams})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = team.members.all()
    return render(request, 'team_detail.html', {'team': team, 'members': members})

def leaderboard(request):
    leaderboard = [
        {'team_name': 'Team Alpha', 'score': 100},
        {'team_name': 'Team Beta', 'score': 80},
    ]
    return render(request, 'leaderboard_view.html', {'leaderboard': leaderboard})

class TeamCreateView(UserPassesTestMixin, CreateView):
    model = Team
    fields = ['name', 'members']
    template_name = 'team_form.html'
    success_url = reverse_lazy('team_list')
    def test_func(self):
        return self.request.user.is_staff

class TeamUpdateView(UserPassesTestMixin, UpdateView):
    model = Team
    fields = ['name', 'members']
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
# DRF VIEW SETS
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
