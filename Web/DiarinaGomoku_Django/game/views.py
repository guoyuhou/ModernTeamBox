from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Game
from users.models import Profile
import random
from django.urls import reverse
from django.contrib.auth.models import User

@login_required
def game_view(request):
    return render(request, 'game/game.html')

def home(request):
    return render(request, 'home.html')

@login_required
def create_game(request):
    game = Game.objects.create(
        black_player=request.user,
        current_player=request.user,
        board=[[None for _ in range(15)] for _ in range(15)]
    )
    return redirect('join_game', game_id=game.id)

@login_required
def join_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.white_player is None and game.black_player != request.user:
        game.white_player = request.user
        game.save()
    return render(request, 'game/game.html', {'game': game})

@login_required
def check_game_status(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return JsonResponse({
        'is_ready': game.white_player is not None,
        'current_player': game.current_player.username
    })

@login_required
def lobby(request):
    online_players = Profile.objects.filter(is_online=True).exclude(user=request.user)
    game_rooms = Game.objects.filter(is_finished=False, white_player__isnull=True)
    return render(request, 'game/lobby.html', {
        'online_players': online_players,
        'game_rooms': game_rooms
    })

@login_required
def random_match(request):
    available_games = Game.objects.filter(is_finished=False, white_player__isnull=True).exclude(black_player=request.user)
    if available_games.exists():
        game = random.choice(available_games)
        game.white_player = request.user
        game.save()
    else:
        game = Game.objects.create(black_player=request.user)
    return JsonResponse({'game_id': game.id})

@login_required
def create_room(request):
    game = Game.objects.create(black_player=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'game_id': game.id})
    else:
        return redirect(reverse('game', args=[game.id]))

@login_required
def ai_battle(request):
    game = Game.objects.create(black_player=request.user, is_ai_opponent=True)
    return JsonResponse({'game_id': game.id})

@login_required
def game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if game.white_player is None and game.black_player != request.user:
        game.white_player = request.user
        game.save()
    context = {
        'game': game,
        'invite_link': request.build_absolute_uri(f'/game/{game.id}/')
    }
    return render(request, 'game/game.html', context)
