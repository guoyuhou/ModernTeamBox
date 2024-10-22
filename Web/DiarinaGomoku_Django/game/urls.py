from django.urls import path
from . import views

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('random-match/', views.random_match, name='random_match'),
    path('create-room/', views.create_room, name='create_room'),
    path('ai-battle/', views.ai_battle, name='ai_battle'),
    path('<int:game_id>/', views.game, name='game'),  # 修改这行
    path('<int:game_id>/join/', views.join_game, name='join_game'),
    path('', views.game_view, name='game'),

]
