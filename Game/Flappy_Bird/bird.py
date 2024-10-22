import pygame
import math
from particle import ParticleSystem

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10
        self.size = 30
        self.angle = 0
        self.colors = [(255, 255, 0), (255, 200, 0), (255, 150, 0)]  # 黄色渐变
        self.wing_angle = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.angle = -self.velocity * 3  # 根据速度调整角度
        self.angle = max(-30, min(self.angle, 30))  # 限制角度范围
        self.wing_angle += 0.3  # 翅膀扇动动画

    def flap(self):
        self.velocity = self.lift

    def draw(self, screen):
        # 绘制身体
        rotated_body = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.ellipse(rotated_body, self.colors[0], (0, 0, self.size, self.size))
        
        # 绘制眼睛
        eye_pos = (self.size * 3 // 4, self.size // 3)
        pygame.draw.circle(rotated_body, (255, 255, 255), eye_pos, self.size // 10)
        pygame.draw.circle(rotated_body, (0, 0, 0), eye_pos, self.size // 20)
        
        # 绘制翅膀
        wing_size = (self.size * 2 // 3, self.size // 2)
        wing_pos = (self.size // 6, self.size // 2)
        wing_angle = math.sin(self.wing_angle) * 30
        wing = pygame.Surface(wing_size, pygame.SRCALPHA)
        pygame.draw.ellipse(wing, self.colors[1], (0, 0, *wing_size))
        rotated_wing = pygame.transform.rotate(wing, wing_angle)
        rotated_body.blit(rotated_wing, wing_pos)

        # 旋转并绘制整个小鸟
        rotated_bird = pygame.transform.rotate(rotated_body, self.angle)
        screen.blit(rotated_bird, rotated_bird.get_rect(center=(int(self.x), int(self.y))))

    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def move_left(self):
        self.horizontal_speed = -5

    def move_right(self):
        self.horizontal_speed = 5

    def stop(self):
        self.horizontal_speed = 0

    def jump(self):
        if self.on_ground:
            self.velocity = self.lift
