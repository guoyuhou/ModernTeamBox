import pygame
import random

class Pipe:
    def __init__(self, x, screen_height):
        self.x = x
        self.screen_height = screen_height
        self.width = 80
        self.gap = 250  # 增加间隔
        self.top_height = random.randint(50, screen_height - self.gap - 50)
        self.bottom_height = screen_height - self.top_height - self.gap
        self.color = (0, 180, 0)  # 深绿色
        self.highlight_color = (50, 220, 50)  # 浅绿色
        self.speed = 1.5  # 降低速度

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        # 绘制上方管道
        self._draw_pipe(screen, self.x, 0, self.width, self.top_height, True)
        
        # 绘制下方管道
        self._draw_pipe(screen, self.x, self.screen_height - self.bottom_height, self.width, self.bottom_height, False)

    def _draw_pipe(self, screen, x, y, width, height, is_top):
        pygame.draw.rect(screen, self.color, (x, y, width, height))
        
        # 添加高光效果
        highlight_width = 10
        if is_top:
            pygame.draw.rect(screen, self.highlight_color, (x, y, highlight_width, height))
        else:
            pygame.draw.rect(screen, self.highlight_color, (x, y, highlight_width, height))
        
        # 添加管道口
        mouth_height = 30
        mouth_color = (0, 150, 0)  # 深绿色
        if is_top:
            pygame.draw.rect(screen, mouth_color, (x - 5, y + height - mouth_height, width + 10, mouth_height))
        else:
            pygame.draw.rect(screen, mouth_color, (x - 5, y, width + 10, mouth_height))

    def off_screen(self):
        return self.x < -self.width

    def collide(self, bird):
        bird_rect = bird.get_rect()
        top_pipe = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_pipe = pygame.Rect(self.x, self.screen_height - self.bottom_height, self.width, self.bottom_height)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)
