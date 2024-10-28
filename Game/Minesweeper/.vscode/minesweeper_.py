import pygame
import random
import sys

# 注释
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # 添加蓝色定义

# 定义游戏参数
CELL_SIZE = 30
WIDTH = 10
HEIGHT = 10
MINES = 10

# 设置窗口
SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")

class Minesweeper:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flags = [[False for _ in range(width)] for _ in range(height)]
        self.remaining_mines = mines
        self.place_mines()

    def place_mines(self):
        placed = 0
        while placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                placed += 1
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] != -1:
                            self.board[ny][nx] += 1

    def reveal(self, x, y):
        print(f"尝试揭开格子: ({x}, {y})")
        if self.flags[y][x]:
            print(f"格子 ({x}, {y}) 已被标记,无法揭开")
            return True

        if self.revealed[y][x]:
            print(f"格子 ({x}, {y}) 已经被揭开")
            return True

        self.revealed[y][x] = True
        if self.board[y][x] == -1:
            print(f"踩到地雷了! 游戏结束")
            return False
        elif self.board[y][x] == 0:
            print(f"揭开空白格子 ({x}, {y}), 继续揭开周围格子")
            self.reveal_surrounding(x, y)
        else:
            print(f"揭开数字格子 ({x}, {y}): {self.board[y][x]}")
        return True

    def reveal_surrounding(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and not self.revealed[ny][nx]:
                    self.reveal(nx, ny)

    def draw_board(self):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[y][x]:
                    pygame.draw.rect(screen, WHITE, rect)
                    if self.board[y][x] > 0:
                        font = pygame.font.Font(None, CELL_SIZE)
                        text = font.render(str(self.board[y][x]), True, BLACK)
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                    elif self.board[y][x] == -1:
                        pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 3)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                
                if self.flags[y][x]:
                    # 绘制旗帜
                    pole_color = (100, 100, 100)
                    flag_color = (255, 0, 0)
                    pole_start = (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4)
                    pole_end = (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE * 3 // 4)
                    pygame.draw.line(screen, pole_color, pole_start, pole_end, 2)
                    flag_points = [
                        (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4),
                        (x * CELL_SIZE + CELL_SIZE * 3 // 4, y * CELL_SIZE + CELL_SIZE // 2),
                        (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE * 3 // 5)
                    ]
                    pygame.draw.polygon(screen, flag_color, flag_points)

        # 显示剩余地雷数
        font = pygame.font.Font(None, 36)
        text = font.render(f"剩余地雷: {self.remaining_mines}", True, BLUE)
        screen.blit(text, (10, SCREEN_HEIGHT - 35))

    def reset_game(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(HEIGHT)]
        self.flags = [[False for _ in range(self.width)] for _ in range(HEIGHT)]
        self.remaining_mines = self.mines
        self.place_mines()

    def toggle_flag(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            if not self.revealed[y][x]:
                self.flags[y][x] = not self.flags[y][x]
                self.remaining_mines += 1 if not self.flags[y][x] else -1
                print(f"标记切换: ({x}, {y}), 当前状态: {'已标记' if self.flags[y][x] else '未标记'}")
                print(f"剩余地雷数: {self.remaining_mines}")
            else:
                print(f"无法标记: ({x}, {y}), 格子已经被揭开")
        else:
            print(f"无法标记: ({x}, {y}), 超出棋盘范围")
        print(f"标记状态: {self.flags[y][x] if 0 <= y < self.height and 0 <= x < self.width else 'N/A'}")

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True

def main_game_loop():
    game = Minesweeper(WIDTH, HEIGHT, MINES)
    running = True
    game_over = False
    game_won = False
    clock = pygame.time.Clock()  # 创建时钟对象

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
                print(f"鼠标点击: 按钮 {event.button}, 位置 ({cell_x}, {cell_y})")
                
                if 0 <= cell_x < WIDTH and 0 <= cell_y < HEIGHT:
                    if event.button == 1:  # 左键点击
                        if game_over or game_won:
                            game.reset_game()
                            game_over = False
                            game_won = False
                            print("游戏重新开始")
                        elif game.reveal(cell_x, cell_y):
                            if game.check_win():
                                game_won = True
                                print("恭喜你赢了!")
                        else:
                            game_over = True
                            print("游戏结束! 你踩到地雷了.")
                    elif event.button == 3:  # 右键点击
                        print("处理右键点击")
                        if not game_over:
                            game.toggle_flag(cell_x, cell_y)
                else:
                    print(f"点击位置 ({cell_x}, {cell_y}) 超出棋盘范围")

        pygame.event.pump()  # 确保所有事件都被处理

        try:
            screen.fill(WHITE)
            game.draw_board()
            
            if game_over:
                show_game_over_popup()
            elif game_won:
                show_win_popup()

            pygame.display.flip()
            clock.tick(30)  # 限制帧率为30FPS
        except Exception as e:
            print(f"绘制错误: {e}")
            running = False

    pygame.quit()

def show_game_over_popup():
    popup_width, popup_height = 300, 150
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill(WHITE)
    pygame.draw.rect(popup, BLACK, (0, 0, popup_width, popup_height), 2)

    font = pygame.font.Font(None, 36)
    text1 = font.render("游戏结束!", True, BLACK)
    text2 = font.render("点击重新开始", True, BLACK)

    popup.blit(text1, (popup_width // 2 - text1.get_width() // 2, 40))
    popup.blit(text2, (popup_width // 2 - text2.get_width() // 2, 90))

    screen.blit(popup, (SCREEN_WIDTH // 2 - popup_width // 2, SCREEN_HEIGHT // 2 - popup_height // 2))

def show_win_popup():
    popup_width, popup_height = 300, 150
    popup = pygame.Surface((popup_width, popup_height))
    popup.fill((200, 200, 200))
    pygame.draw.rect(popup, BLACK, (0, 0, popup_width, popup_height), 2)

    font = pygame.font.SysFont('simhei', 36)
    text1 = font.render("你赢了!", True, (255, 0, 0))
    text2 = font.render("点击重新开始", True, (0, 0, 255))

    popup.blit(text1, (popup_width // 2 - text1.get_width() // 2, 40))
    popup.blit(text2, (popup_width // 2 - text2.get_width() // 2, 90))

    screen.blit(popup, (SCREEN_WIDTH // 2 - popup_width // 2, SCREEN_HEIGHT // 2 - popup_height // 2))

if __name__ == "__main__":
    main_game_loop()
