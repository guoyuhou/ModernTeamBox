from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Cast
from game.models import Game
from django.db import models

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账号已创建，您现在可以登录了！')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'您的账号已更新！')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    user = request.user
    total_games = user.profile.wins + user.profile.losses
    win_rate = (user.profile.wins / total_games * 100) if total_games > 0 else 0
    

    context = {
        'user': user,
        'wins': user.profile.wins,
        'losses': user.profile.losses,
        'total_games': total_games,
        'win_rate': round(win_rate, 2)
    }
    return render(request, 'users/profile.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            Profile.objects.get_or_create(user=request.user)
            request.user.profile.is_online = True
            request.user.profile.save()
            return redirect('home')
        else:
            messages.info(request, '用户名或密码错误')
            return redirect('login')

def user_logout(request):
    request.user.is_active = False
    request.user.save()
    logout(request)
    return redirect('home')

def leaderboard(request):
    profiles = Profile.objects.annotate(
        total_games=F('wins') + F('losses'),
        win_rate=ExpressionWrapper(
            Cast(F('wins'), FloatField()) / Cast((F('wins') + F('losses')), FloatField()) * 100,
            output_field=FloatField()
        )
    ).filter(total_games__gt=0).order_by('-win_rate', '-wins')[:10]

    context = {
        'profiles': profiles
    }
    return render(request, 'users/leaderboard.html', context)

@login_required
def game_history(request):
    user = request.user
    games = Game.objects.filter(is_finished=True).filter(
        models.Q(black_player=user) | models.Q(white_player=user)
    ).order_by('-created_at')

    game_records = []
    for game in games:
        opponent = game.white_player if game.black_player == user else game.black_player
        result = "胜利" if game.winner == user else "失败"
        color = "黑棋" if game.black_player == user else "白棋"
        game_records.append({
            'id': game.id,
            'opponent': opponent.username,
            'result': result,
            'color': color,
            'date': game.created_at
        })

    context = {
        'game_records': game_records
    }
    return render(request, 'users/game_history.html', context)
