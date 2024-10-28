import pygame
import random

# 初始化 Pygame
pygame.init()

# 颜色定义 - 使用更现代的配色方案
COLORS = {
    0: (205, 193, 180),      # 空格子颜色
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# 游戏配置
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
GRID_SIZE = 4
CELL_SIZE = 100
PADDING = 10

# 颜色定义
BACKGROUND_COLOR = (250, 248, 239)  # 米色背景
GRID_COLOR = (187, 173, 160)        # 网格背景色
TEXT_COLOR = (119, 110, 101)        # 深灰色文字

# 动画相关常量
ANIMATION_SPEED = 15
SPAWN_ANIMATION_SPEED = 0.2

# 创建窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('2048')

class Tile:
    def __init__(self, value, pos):
        self.value = value
        self.current_pos = list(pos)
        self.target_pos = list(pos)
        self.scale = 0.1 if value != 0 else 1
    
    def update(self):
        self.current_pos[0] += (self.target_pos[0] - self.current_pos[0]) / ANIMATION_SPEED
        self.current_pos[1] += (self.target_pos[1] - self.current_pos[1]) / ANIMATION_SPEED
        if self.scale < 1:
            self.scale += SPAWN_ANIMATION_SPEED
            if self.scale > 1:
                self.scale = 1

class Game2048:
    def __init__(self):
        self.grid = [[Tile(0, (i, j)) for j in range(GRID_SIZE)] 
                    for i in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()
    
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) 
                      for j in range(GRID_SIZE) if self.grid[i][j].value == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            value = 2 if random.random() < 0.9 else 4
            self.grid[i][j] = Tile(value, (i, j))

    def merge(self, line):
        # 移除零
        non_zero = [x for x in line if x != 0]
        
        # 合并相同的数字
        for i in range(len(non_zero) - 1):
            if non_zero[i] == non_zero[i + 1]:
                non_zero[i] *= 2
                non_zero[i + 1] = 0
        
        # 再次移除零并补充零
        non_zero = [x for x in non_zero if x != 0]
        return non_zero + [0] * (GRID_SIZE - len(non_zero))

    def move(self, direction):
        moved = False
        if direction in ['UP', 'DOWN']:
            for j in range(GRID_SIZE):
                column = [self.grid[i][j].value for i in range(GRID_SIZE)]
                if direction == 'UP':
                    new_column = self.merge(column)
                else:
                    new_column = self.merge(column[::-1])[::-1]
                
                for i in range(GRID_SIZE):
                    if self.grid[i][j].value != new_column[i]:
                        moved = True
                        if new_column[i] > self.grid[i][j].value:
                            self.score += new_column[i]
                        self.grid[i][j] = Tile(new_column[i], (i, j))
        
        else:  # LEFT or RIGHT
            for i in range(GRID_SIZE):
                row = [self.grid[i][j].value for j in range(GRID_SIZE)]
                if direction == 'LEFT':
                    new_row = self.merge(row)
                else:
                    new_row = self.merge(row[::-1])[::-1]
                
                for j in range(GRID_SIZE):
                    if self.grid[i][j].value != new_row[j]:
                        moved = True
                        if new_row[j] > self.grid[i][j].value:
                            self.score += new_row[j]
                        self.grid[i][j] = Tile(new_row[j], (i, j))

        if moved:
            self.add_new_tile()
        
        return moved

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        
        # 绘制标题
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render('2048', True, TEXT_COLOR)
        screen.blit(title_text, (20, 20))
        
        # 绘制分数
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f'分数: {self.score}', True, TEXT_COLOR)
        screen.blit(score_text, (WINDOW_WIDTH - 200, 40))
        
        # 绘制游戏网格背景
        grid_background = pygame.Rect(
            (WINDOW_WIDTH - CELL_SIZE * GRID_SIZE - PADDING * 2) // 2,
            120,
            CELL_SIZE * GRID_SIZE + PADDING * 2,
            CELL_SIZE * GRID_SIZE + PADDING * 2
        )
        pygame.draw.rect(screen, GRID_COLOR, grid_background, border_radius=10)
        
        # 绘制每个格子
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = self.grid[i][j]
                value = tile.value
                
                base_x = (WINDOW_WIDTH - CELL_SIZE * GRID_SIZE) // 2
                base_y = 120
                
                x = base_x + j * CELL_SIZE + PADDING
                y = base_y + i * CELL_SIZE + PADDING
                
                size = CELL_SIZE - PADDING * 2
                rect = pygame.Rect(x, y, size, size)
                
                pygame.draw.rect(screen, COLORS.get(value, COLORS[0]), rect, border_radius=8)
                
                if value != 0:
                    font_size = 48 if value < 100 else 36 if value < 1000 else 30
                    font = pygame.font.Font(None, font_size)
                    text_color = (119, 110, 101) if value <= 4 else (249, 246, 242)
                    text = font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.fill((255, 255, 255))
            overlay.set_alpha(180)
            screen.blit(overlay, (0, 0))
            
            font = pygame.font.Font(None, 72)
            game_over_text = font.render('游戏结束!', True, TEXT_COLOR)
            restart_text = font.render('按R重新开始', True, TEXT_COLOR)
            
            screen.blit(game_over_text, 
                       (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                        WINDOW_HEIGHT // 2 - 50))
            screen.blit(restart_text, 
                       (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                        WINDOW_HEIGHT // 2 + 50))

    def check_game_over(self):
        # 检查是否还有空格
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j].value == 0:
                    return False
        
        # 检查是否还能合并
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j].value
                if (i < GRID_SIZE - 1 and value == self.grid[i + 1][j].value) or \
                   (j < GRID_SIZE - 1 and value == self.grid[i][j + 1].value):
                    return False
        
        return True

def main():
    game = Game2048()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Game2048()
                elif not game.game_over:
                    if event.key == pygame.K_UP:
                        game.move('UP')
                    elif event.key == pygame.K_DOWN:
                        game.move('DOWN')
                    elif event.key == pygame.K_LEFT:
                        game.move('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        game.move('RIGHT')
                    
                    game.game_over = game.check_game_over()
        
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
