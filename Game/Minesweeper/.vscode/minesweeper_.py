import pygame
import random
import sys

<<<<<<< HEAD
# 初始化 Pygame
pygame.init()

# 定义颜色
白色 = (255, 255, 255)
灰色 = (200, 200, 200)
黑色 = (0, 0, 0)
红色 = (255, 0, 0)
蓝色 = (0, 0, 255)  # 添加这行来定义蓝色

# 定义游戏参数
格子大小 = 30
宽度 = 10
高度 = 10
地雷数 = 10

# 设置窗口
屏幕宽度 = 宽度 * 格子大小
屏幕高度 = 高度 * 格子大小
屏幕 = pygame.display.set_mode((屏幕宽度, 屏幕高度))
pygame.display.set_caption("扫雷游戏")

class 扫雷游戏:
    def __init__(self, 宽度, 高度, 地雷数):
        self.宽度 = 宽度
        self.高度 = 高度
        self.地雷数 = 地雷数
        self.棋盘 = [[0 for _ in range(宽度)] for _ in range(高度)]
        self.已揭示 = [[False for _ in range(宽度)] for _ in range(高度)]
        self.标记 = [[False for _ in range(宽度)] for _ in range(高度)]
        self.剩余地雷数 = 地雷数
        self.放置地雷()

    def 放置地雷(self):
        已放置 = 0
        while 已放置 < self.地雷数:
            x = random.randint(0, self.宽度 - 1)
            y = random.randint(0, self.高度 - 1)
            if self.棋盘[y][x] != -1:
                self.棋盘[y][x] = -1
                已放置 += 1
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.宽度 and 0 <= ny < self.高度 and self.棋盘[ny][nx] != -1:
                            self.棋盘[ny][nx] += 1

    def 揭示(self, x, y):
        print(f"尝试揭示格子：({x}, {y})")
        if self.标记[y][x]:
            print(f"格子 ({x}, {y}) 已被标记，无法揭示")
            return True

        if self.已揭示[y][x]:
            print(f"格子 ({x}, {y}) 已经被揭示")
            return True

        self.已揭示[y][x] = True
        if self.棋盘[y][x] == -1:
            print(f"踩到地雷！游戏结束")
            return False
        elif self.棋盘[y][x] == 0:
            print(f"揭示空白格子 ({x}, {y})，继续揭示周围格子")
            self.揭示周围格子(x, y)
        else:
            print(f"揭示数字格子 ({x}, {y}): {self.棋盘[y][x]}")
        return True

    def 揭示周围格子(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.宽度 and 0 <= ny < self.高度 and not self.已揭示[ny][nx]:
                    self.揭示(nx, ny)

    def 绘制棋盘(self):
        for y in range(self.高度):
            for x in range(self.宽度):
                rect = pygame.Rect(x * 格子大小, y * 格子大小, 格子大小, 格子大小)
                if self.已揭示[y][x]:
                    pygame.draw.rect(屏幕, 白色, rect)
                    if self.棋盘[y][x] > 0:
                        字体 = pygame.font.Font(None, 格子大小)
                        文本 = 字体.render(str(self.棋盘[y][x]), True, 黑色)
                        文本矩形 = 文本.get_rect(center=rect.center)
                        屏幕.blit(文本, 文本矩形)
                    elif self.棋盘[y][x] == -1:
                        pygame.draw.circle(屏幕, 红色, rect.center, 格子大小 // 3)
                else:
                    pygame.draw.rect(屏幕, 灰色, rect)
                    pygame.draw.rect(屏幕, 黑色, rect, 1)
                
                if self.标记[y][x]:
                    # 绘制小红旗
                    旗杆颜色 = (100, 100, 100)
                    旗帜颜色 = (255, 0, 0)
                    旗杆起点 = (x * 格子大小 + 格子大小 // 4, y * 格子大小 + 格子大小 // 4)
                    旗杆终点 = (x * 格子大小 + 格子大小 // 4, y * 格子大小 + 格子大小 * 3 // 4)
                    pygame.draw.line(屏幕, 旗杆颜色, 旗杆起点, 旗杆终点, 2)
                    旗帜点 = [
                        (x * 格子大小 + 格子大小 // 4, y * 格子大小 + 格子大小 // 4),
                        (x * 格子大小 + 格子大小 * 3 // 4, y * 格子大小 + 格子大小 // 2),
                        (x * 格子大小 + 格子大小 // 4, y * 格子大小 + 格子大小 * 3 // 5)
                    ]
                    pygame.draw.polygon(屏幕, 旗帜颜色, 旗帜点)

        # 显示剩余地雷数
        字体 = pygame.font.Font(None, 36)
        文本 = 字体.render(f"剩余地雷: {self.剩余地雷数}", True, 蓝色)
        屏幕.blit(文本, (10, 屏幕高度 - 35))

    def 重置游戏(self):
        self.棋盘 = [[0 for _ in range(self.宽度)] for _ in range(self.高度)]
        self.已揭示 = [[False for _ in range(self.宽度)] for _ in range(高度)]
        self.标记 = [[False for _ in range(self.宽度)] for _ in range(高度)]
        self.剩余地雷数 = self.地雷数
        self.放置地雷()

    def 切换标记(self, x, y):
        if 0 <= x < self.宽度 and 0 <= y < self.高度:
            if not self.已揭示[y][x]:
                self.标记[y][x] = not self.标记[y][x]
                self.剩余地雷数 += 1 if not self.标记[y][x] else -1
                print(f"标记切换：({x}, {y}), 当前状态：{'已标记' if self.标记[y][x] else '未标记'}")
                print(f"剩余地雷数：{self.剩余地雷数}")
            else:
                print(f"无法标记：({x}, {y}), 该格子已揭示")
        else:
            print(f"无法标记：({x}, {y}), 超出棋盘范围")
        print(f"标记状态：{self.标记[y][x] if 0 <= y < self.高度 and 0 <= x < self.宽度 else 'N/A'}")

    def 检查胜利(self):
        for y in range(self.高度):
            for x in range(self.宽度):
                if self.棋盘[y][x] != -1 and not self.已揭示[y][x]:
                    return False
        return True

def 主游戏循环():
    游戏 = 扫雷游戏(宽度, 高度, 地雷数)
    运行中 = True
    游戏结束 = False
    游戏胜利 = False
    时钟 = pygame.time.Clock()  # 创建时钟对象

    while 运行中:
        for 事件 in pygame.event.get():
            if 事件.type == pygame.QUIT:
                运行中 = False
            elif 事件.type == pygame.MOUSEBUTTONDOWN:
                x, y = 事件.pos
                格子x, 格子y = x // 格子大小, y // 格子大小
                print(f"鼠标点击：按钮 {事件.button}, 位置 ({格子x}, {格子y})")
                
                if 0 <= 格子x < 宽度 and 0 <= 格子y < 高度:
                    if 事件.button == 1:  # 左键点击
                        if 游戏结束 or 游戏胜利:
                            游戏.重置游戏()
                            游戏结束 = False
                            游戏胜利 = False
                            print("游戏重新开始")
                        elif 游戏.揭示(格子x, 格子y):
                            if 游戏.检查胜利():
                                游戏胜利 = True
                                print("恭喜你赢了！")
                        else:
                            游戏结束 = True
                            print("游戏结束！你踩到地雷了。")
                    elif 事件.button == 3:  # 右键点击
                        print("处理右键点击")
                        if not 游戏结束:
                            游戏.切换标记(格子x, 格子y)
                else:
                    print(f"点击位置 ({格子x}, {格子y}) 超出棋盘范围")
=======
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
>>>>>>> bda5d9b8f689d7f615367d5fe9a7bb24438f8e89

        pygame.event.pump()  # 确保所有事件都被处理

        try:
<<<<<<< HEAD
            屏幕.fill(白色)
            游戏.绘制棋盘()
            
            if 游戏结束:
                显示游戏结束弹窗()
            elif 游戏胜利:
                显示胜利弹窗()

            pygame.display.flip()
            时钟.tick(30)  # 限制帧率为30FPS
        except Exception as e:
            print(f"绘制错误：{e}")
            运行中 = False

    pygame.quit()

def 显示游戏结束弹窗():
    弹窗宽度, 弹窗高度 = 300, 150
    弹窗 = pygame.Surface((弹窗宽度, 弹窗高度))
    弹窗.fill(白色)
    pygame.draw.rect(弹窗, 黑色, (0, 0, 弹窗宽度, 弹窗高度), 2)

    字体 = pygame.font.Font(None, 36)
    文本1 = 字体.render("游戏结束！点击重新开始", True, 黑色)
    文本2 = 字体.render("点击重新开始", True, 黑色)

    弹窗.blit(文本1, (弹窗宽度 // 2 - 文本1.get_width() // 2, 40))
    弹窗.blit(文本2, (弹窗宽度 // 2 - 文本2.get_width() // 2, 90))

    屏幕.blit(弹窗, (屏幕宽度 // 2 - 弹窗宽度 // 2, 屏幕高度 // 2 - 弹窗高度 // 2))

def 显示胜利弹窗():
    弹窗宽度, 弹窗高度 = 300, 150
    弹窗 = pygame.Surface((弹窗宽度, 弹窗高度))
    弹窗.fill((200, 200, 200))
    pygame.draw.rect(弹窗, 黑色, (0, 0, 弹窗宽度, 弹窗高度), 2)

    字体 = pygame.font.SysFont('simhei', 36)
    文本1 = 字体.render("恭喜你赢了！", True, (255, 0, 0))
    文本2 = 字体.render("点击重新开始", True, (0, 0, 255))

    弹窗.blit(文本1, (弹窗宽度 // 2 - 文本1.get_width() // 2, 40))
    弹窗.blit(文本2, (弹窗宽度 // 2 - 文本2.get_width() // 2, 90))

    屏幕.blit(弹窗, (屏幕宽度 // 2 - 弹窗宽度 // 2, 屏幕高度 // 2 - 弹窗高度 // 2))

if __name__ == "__main__":
    主游戏循环()
=======
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
>>>>>>> bda5d9b8f689d7f615367d5fe9a7bb24438f8e89
