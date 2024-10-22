from django.db import models
from django.contrib.auth.models import User
import random

class Game(models.Model):
    black_player = models.ForeignKey(User, related_name='black_games', on_delete=models.CASCADE)
    white_player = models.ForeignKey(User, related_name='white_games', on_delete=models.CASCADE, null=True, blank=True)
    current_player = models.ForeignKey(User, related_name='current_games', on_delete=models.CASCADE)
    board = models.JSONField(default=list)
    is_finished = models.BooleanField(default=False)
    winner = models.ForeignKey(User, related_name='won_games', on_delete=models.SET_NULL, null=True, blank=True)
    is_ai_opponent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # 新增字段

    def __str__(self):
        return f"Game {self.id}: {self.black_player} vs {self.white_player or 'AI'}"

    def initialize_board(self):
        self.board = [[None for _ in range(15)] for _ in range(15)]

    def make_move(self, row, col, player):
        if self.board[row][col] is None and not self.is_finished:
            self.board[row][col] = player.username
            self.current_player = self.white_player if self.current_player == self.black_player else self.black_player
            self.check_winner(row, col, player)
            self.save()
            return True
        return False

    def check_winner(self, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 5):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < 15 and 0 <= c < 15 and self.board[r][c] == player:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < 15 and 0 <= c < 15 and self.board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def ai_move(self):
        # 简单的AI逻辑：随机选择一个空位
        empty_cells = [(i, j) for i in range(15) for j in range(15) if self.board[i][j] is None]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col, self.white_player)
            return row, col
        return None

    def save(self, *args, **kwargs):
        if not self.id:
            self.current_player = self.black_player
            if not self.board:
                self.board = [[None for _ in range(15)] for _ in range(15)]
        super().save(*args, **kwargs)

    def end_game(self, winner):
        self.is_finished = True
        self.winner = winner
        self.save()

        winner.profile.wins += 1
        winner.profile.save()

        loser = self.black_player if winner == self.white_player else self.white_player
        loser.profile.losses += 1
        loser.profile.save()
