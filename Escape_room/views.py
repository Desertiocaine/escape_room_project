from rest_framework import viewsets
from .models import Room, Puzzle, Booking, Team
from .serializers import RoomSerializer, PuzzleSerializer, BookingSerializer, TeamSerializer
from django.shortcuts import render , get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    puzzles = room.puzzles.all()
    return render(request, 'room_detail.html', {'room': room, 'puzzles': puzzles})

def solve_puzzle(request, puzzle_id):
    puzzle = get_object_or_404(Puzzle, id=puzzle_id)
    if request.method == "POST":
        user_answer = request.POST.get("answer", "").strip()
        if user_answer.lower() == puzzle.answer.lower():
            # You can add logic to track solved puzzles here
            return render(request, "puzzle_solved.html", {"puzzle": puzzle, "correct": True})
        else:
            return render(request, "puzzle_solved.html", {"puzzle": puzzle, "correct": False})
    return HttpResponseRedirect(reverse("room_detail", args=[puzzle.room.id]))

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'team_list.html', {'teams': teams})

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = team.members.all()
    return render(request, 'team_detail.html', {'team': team, 'members': members})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('team_list') # or any page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class PuzzleViewSet(viewsets.ModelViewSet):
    # Creates full CRUD API functionality for Puzzle model
    queryset = Puzzle.objects.all()
    serializer_class = PuzzleSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class TeamViewSet(viewsets.ModelViewSet):
    # Creates full CRUD API functionality for Team model
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

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
# Create your views here.

class TeamCreateView(CreateView):
    model = Team
    fields = ['name', 'members', 'room']
    template_name = 'team_form.html'
    success_url = reverse_lazy('team_list')

class TeamUpdateView(UpdateView):
    model = Team
    fields = ['name', 'members', 'room']
    template_name = 'team_form.html'
    success_url = reverse_lazy('team_list')

class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'team_confirm_delete.html'
    success_url = reverse_lazy('team_list')