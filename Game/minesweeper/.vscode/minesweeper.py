import pygame
import sys

import random

class 扫雷游戏:
    def __init__(self, 宽度, 高度, 地雷数):
        self.宽度 = 宽度
        self.高度 = 高度
        self.地雷数 = 地雷数
        self.棋盘 = [[0 for _ in range(宽度)] for _ in range(高度)]
        self.已揭示 = [[False for _ in range(宽度)] for _ in range(高度)]
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
        if not (0 <= x < self.宽度 and 0 <= y < self.高度) or self.已揭示[y][x]:
            return
        self.已揭示[y][x] = True
        if self.棋盘[y][x] == -1:
            return False
        if self.棋盘[y][x] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    self.揭示(x + dx, y + dy)
        return True

    def 打印棋盘(self):
        for y in range(self.高度):
            for x in range(self.宽度):
                if self.已揭示[y][x]:
                    print('*' if self.棋盘[y][x] == -1 else self.棋盘[y][x], end=' ')
                else:
                    print('.', end=' ')
            print()

def 玩游戏():
    游戏 = 扫雷游戏(10, 10, 10)
    while True:
        游戏.打印棋盘()
        x = int(input("请输入x坐标: "))
        y = int(input("请输入y坐标: "))
        if not 游戏.揭示(x, y):
            print("游戏结束！你踩到地雷了。")
            游戏.打印棋盘()
            break

if __name__ == "__main__":
    玩游戏()

