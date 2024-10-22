import pygame
import sys
from bird import Bird
from pipe import Pipe
from cloud import Cloud
from particle import ParticleSystem
from ui import UI

# 初始化Pygame
pygame.init()

# 设置屏幕大小和标题
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# 设置颜色
BLUE = (135, 206, 235)  # 天蓝色背景

# 设置时钟
clock = pygame.time.Clock()

# 创建UI对象
ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)

def main():
    game_state = "start"
    bird = Bird(50, SCREEN_HEIGHT // 2)
    pipes = []
    clouds = [Cloud(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(5)]
    explosion_particles = ParticleSystem()
    score = 0
    high_score = 0
    pipe_spawn_timer = 0
    background_offset = 0
    background_speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "start":
                    start_button = ui.draw_start_screen(screen)
                    if start_button.is_clicked(event.pos):
                        game_state = "playing"
                        bird = Bird(50, SCREEN_HEIGHT // 2)
                        pipes = []
                        score = 0
                        pipe_spawn_timer = 0
                elif game_state == "game_over":
                    restart_button = ui.draw_game_over(screen, score, high_score)
                    if restart_button.is_clicked(event.pos):
                        game_state = "playing"
                        bird = Bird(50, SCREEN_HEIGHT // 2)
                        pipes = []
                        score = 0
                        pipe_spawn_timer = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "playing":
                    bird.flap()

        screen.fill(BLUE)

        # 绘制移动的背景
        background_offset = (background_offset + background_speed) % SCREEN_WIDTH
        for i in range(-1, 2):
            pygame.draw.rect(screen, (100, 200, 100), (i * SCREEN_WIDTH - background_offset, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

        for cloud in clouds:
            cloud.update()
            cloud.draw(screen)

        if game_state == "start":
            ui.draw_start_screen(screen)
        elif game_state == "playing":
            bird.update()

            pipe_spawn_timer += 1
            if pipe_spawn_timer > 120:  # 每120帧生成一个新管道
                pipes.append(Pipe(SCREEN_WIDTH, SCREEN_HEIGHT))
                pipe_spawn_timer = 0

            for pipe in pipes:
                pipe.update()
                if pipe.collide(bird):
                    game_state = "game_over"
                    explosion_particles.add_particles(bird.x, bird.y, bird.colors[0], 50)
                    if score > high_score:
                        high_score = score

            pipes = [pipe for pipe in pipes if not pipe.off_screen()]

            if pipes and bird.x > pipes[0].x + pipes[0].width:
                score += 1
                pipes.pop(0)

            if bird.y > SCREEN_HEIGHT or bird.y < 0:
                game_state = "game_over"
                explosion_particles.add_particles(bird.x, bird.y, bird.colors[0], 50)
                if score > high_score:
                    high_score = score

            # 绘制游戏元素
            for pipe in pipes:
                pipe.draw(screen)
            bird.draw(screen)
            ui.draw_game_ui(
                screen, score)

        elif game_state == "game_over":
            # 绘制游戏元素（静态）
            for pipe in pipes:
                pipe.draw(screen)
            bird.draw(screen)
            ui.draw_game_over(screen, score, high_score)

        explosion_particles.update()
        explosion_particles.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
