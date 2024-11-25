#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@fileName: main.py
@project: GomokuGame
@version: 1.0.4
@description: 使用 Pygame 实现的五子棋游戏。
该游戏允许两名玩家（黑方和白方）轮流在 17*17 的棋盘上放置棋子。
第一个达到连续五个棋子的一方获胜。
@author: PythonDeveloper29042
@authorEmail: pythondeveloper.29042@outlook.com
@commitDate: 2024/11/10
@github: https://github.com/PythonDeveloper29042/GomokuGame_zh_CN.git
"""

import pygame
import game

ROWS = 17
SIDE = 30

SCREEN_WIDTH = ROWS * SIDE  # 屏幕宽度
SCREEN_HEIGHT = ROWS * SIDE  # 屏幕高度

EMPTY = -1
BLACK = (0, 0, 0)  # 代表黑棋的颜色
WHITE = (255, 255, 255)  # 代表白棋的颜色
DIRE = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 检查连续棋子的方向


class Gomoku(game.Game):
    def __init__(self, title: str, size: tuple[int, int], fps: int = 15):
        """
        使用指定的标题、大小和 FPS 初始化五子棋游戏。

        Args:
            title (str): 游戏窗口的标题。
            size (tuple[int, int]): 游戏窗口的尺寸（宽度，高度）。
            fps (int, 可选): 游戏更新的每秒帧数。默认为 15。
        """
        super(Gomoku, self).__init__(title, size, fps)
        self.board = [
            [EMPTY for _ in range(ROWS)] for _ in range(ROWS)
        ]  # 将棋盘初始化为二维列表
        self.select = (-1, -1)
        self.black = True
        self.draw_board()
        self.bind_click(1, self.click)

    def click(self, x: int, y: int):
        """
        处理点击事件，在棋盘上放置棋子。

        Args:
            x (int): 点击位置的 x 坐标。
            y (int): 点击位置的 y 坐标。
        """
        if self.end:
            return
        i, j = y // SIDE, x // SIDE
        if self.board[i][j] != EMPTY:
            return
        self.board[i][j] = BLACK if self.black else WHITE
        self.draw_chess(self.board[i][j], i, j)
        self.black = not self.black

        chess = self.check_win()
        if chess:  # 检查胜利条件
            self.end = True
            i, j = chess[0]
            winner = "黑方" if self.board[i][j] == BLACK else "白方"
            pygame.display.set_caption(f"五子棋 ---- {winner} 获胜!")
            for c in chess:
                i, j = c
                self.draw_chess((100, 255, 255), i, j)  # 高亮显示获胜的棋子
                self.timer.tick(5)

    def check_win(self) -> list[tuple[int, int]] | None:
        """
        通过搜索五个连续的棋子来检查是否有获胜者。

        Args:
            list[tuple[int, int]] | None: 形成获胜线的坐标列表，或无获胜者时返回 None。
        """
        for i in range(ROWS):
            for j in range(ROWS):
                win = self.check_chess(i, j)
                if win:
                    return win
        return None

    def check_chess(self, i: int, j: int) -> list[tuple[int, int]] | None:
        """
        从给定位置检查所有方向的连续棋子。

        Args:
            i (int): 棋子的行索引。
            j (int): 棋子的列索引。

        Returns:
            list[tuple[int, int]] | None: 如果找到连续的棋子，返回形成连续线的坐标列表，否则返回 None。
        """
        if self.board[i][j] == EMPTY:
            return None
        color = self.board[i][j]
        for dire in DIRE:
            x, y = i, j
            chess = []
            while 0 <= x < ROWS and 0 <= y < ROWS and self.board[x][y] == color:
                chess.append((x, y))
                x, y = x + dire[0], y + dire[1]
            if len(chess) >= 5:
                return chess
        return None

    def draw_chess(self, color: tuple[int, int, int], i: int, j: int):
        """
        在棋盘的指定位置绘制一个棋子。

        Args:
            color (tuple[int, int, int]): 棋子的 RGB 颜色。
            i (int): 棋子的行索引。
            j (int): 棋子的列索引。
        """
        center = (j * SIDE + SIDE // 2, i * SIDE + SIDE // 2)
        pygame.draw.circle(self.screen, color, center, SIDE // 2 - 2)
        pygame.display.update(pygame.Rect(j * SIDE, i * SIDE, SIDE, SIDE))

    def draw_board(self):
        """
        绘制初始的棋盘，包括网格线和中心点。
        """
        self.screen.fill((139, 87, 66))  # 用棕色填充背景
        for i in range(ROWS):
            start = (i * SIDE + SIDE // 2, SIDE // 2)
            end = (i * SIDE + SIDE // 2, ROWS * SIDE - SIDE // 2)
            pygame.draw.line(self.screen, 0x000000, start, end)  # 绘制垂直线
            start = (SIDE // 2, i * SIDE + SIDE // 2)
            end = (ROWS * SIDE - SIDE // 2, i * SIDE + SIDE // 2)
            pygame.draw.line(self.screen, 0x000000, start, end)  # 绘制水平线
        center = ((ROWS // 2) * SIDE + SIDE // 2, (ROWS // 2) * SIDE + SIDE // 2)
        pygame.draw.circle(self.screen, (0, 0, 0), center, 4)  # 绘制中心点
        pygame.display.update()


if __name__ == "__main__":
    print(
        "\n欢迎来到终极五子棋比赛！！！\n左键点击棋盘上的任意点开始游戏。\n"
    )  # 欢迎信息

    gomoku = Gomoku("五子棋", (SCREEN_WIDTH, SCREEN_HEIGHT))
    gomoku.run()  # 运行游戏

# 创建可执行文件:
# pip install pyinstaller
# pyinstaller -F -w main.py
