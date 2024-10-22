import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class UI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

    def draw_start_screen(self, screen):
        screen.fill((135, 206, 235))  # 天蓝色背景
        title = self.font.render("Flappy Bird", True, (255, 255, 255))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))

        start_button = Button(self.screen_width // 2 - 100, 300, 200, 50, "Start Game", (0, 255, 0), (255, 255, 255))
        start_button.draw(screen)

        return start_button

    def draw_game_ui(self, screen, score):
        score_text = self.small_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def draw_game_over(self, screen, score, high_score):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, 200))

        score_text = self.small_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 300))

        high_score_text = self.small_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (self.screen_width // 2 - high_score_text.get_width() // 2, 350))

        restart_button = Button(self.screen_width // 2 - 100, 400, 200, 50, "Restart", (0, 255, 0), (255, 255, 255))
        restart_button.draw(screen)

        return restart_button
