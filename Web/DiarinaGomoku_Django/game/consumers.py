import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game
from django.contrib.auth.models import User

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        
        if action == 'move':
            row = int(data['row'])
            col = int(data['col'])
            player = data['player']
            
            game = await self.get_game()
            current_player = await self.get_current_player(game)
            
            if current_player == self.scope['user'] and not game.is_finished:
                if await self.make_move(game, row, col, player):
                    is_winner = await self.check_winner(game, row, col, player)
                    loser_username = None
                    if is_winner:
                        loser_username = game.white_player.username if player == 'black' else game.black_player.username
                    await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            'type': 'game_move',
                            'row': row,
                            'col': col,
                            'player': player,
                            'is_winner': is_winner,
                            'winner_username': self.scope['user'].username if is_winner else None,
                            'loser_username': loser_username
                        }
                    )
                    if is_winner:
                        await self.end_game(game, self.scope['user'])

    async def game_move(self, event):
        await self.send(text_data=json.dumps({
            'action': 'move',
            'row': event['row'],
            'col': event['col'],
            'player': event['player'],
            'is_winner': event['is_winner'],
            'winner_username': event['winner_username'],
            'loser_username': event['loser_username'] if event['is_winner'] else None
        }))

    @database_sync_to_async
    def get_game(self):
        return Game.objects.get(pk=self.game_id)

    @database_sync_to_async
    def get_current_player(self, game):
        return game.current_player

    @database_sync_to_async
    def make_move(self, game, row, col, player):
        if game.board[row][col] is None:
            game.board[row][col] = player
            game.current_player = game.white_player if player == 'black' else game.black_player
            game.save()
            return True
        return False

    @database_sync_to_async
    def check_winner(self, game, row, col, player):
        return game.check_winner(row, col, player)

    @database_sync_to_async
    def end_game(self, game, winner):
        game.end_game(winner)

class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("lobby", self.channel_name)
        await self.accept()
        await self.update_online_users()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("lobby", self.channel_name)
        await self.update_online_users()

    @database_sync_to_async
    def get_online_users(self):
        return list(User.objects.filter(is_active=True).values_list('username', flat=True))

    async def update_online_users(self):
        online_users = await self.get_online_users()
        await self.channel_layer.group_send(
            "lobby",
            {
                "type": "send_online_users",
                "online_users": online_users
            }
        )

    async def send_online_users(self, event):
        await self.send(text_data=json.dumps({
            "type": "online_users",
            "online_users": event["online_users"]
        }))
