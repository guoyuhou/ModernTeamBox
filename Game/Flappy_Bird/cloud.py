import pygame
import random

class Cloud:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width
        self.y = random.randint(0, screen_height // 2)
        self.speed = random.uniform(0.5, 1.5)
        self.size = random.randint(50, 100)
        self.color = (255, 255, 255)  # 白色

    def update(self):
        self.x -= self.speed
        if self.x < -self.size:
            self.x = self.screen_width
            self.y = random.randint(0, self.screen_height // 2)

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.size, self.size // 2))
        pygame.draw.ellipse(screen, self.color, (self.x + self.size // 4, self.y - self.size // 4, self.size // 2, self.size // 2))
        pygame.draw.ellipse(screen, self.color, (self.x + self.size // 2, self.y, self.size // 2, self.size // 3))