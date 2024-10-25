import pygame
import random
import sys

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

        pygame.event.pump()  # 确保所有事件都被处理

        try:
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
