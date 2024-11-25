#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@fileName: game.py
@project: GomokuGame
@description: 提供一个基础的游戏类，具有键盘和鼠标事件、暂停、全屏模式和分数显示功能。
包括一个测试类作为基本游戏设置的示例。
@author: Pythondeveloper29042
@authorEmail: pythondeveloper.29042@outlook.com
@commitDate: 2024/11/10
@github: https://github.com/PythonDeveloper29042/GomokuGame_zh_CN.git
"""

import pygame
from pygame.locals import *
from sys import exit
from typing import Callable, Optional, Tuple

# 定义四邻和八邻方向的移动
FOUR_NEIGH = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
EIGHT_NEIGH = list(FOUR_NEIGH.values()) + [(1, 1), (1, -1), (-1, 1), (-1, -1)]

# 定义键盘方向映射
DIRECTION = {
    pygame.K_UP: "up",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_DOWN: "down",
}


def hex2rgb(color: int) -> Tuple[int, int, int]:
    """
    将十六进制颜色转换为RGB元组。

    Args:
        color (int): 十六进制格式的颜色。

    Returns:
        Tuple[int, int, int]: 对应的RGB颜色。
    """
    b = color % 256
    color = color >> 8
    g = color % 256
    color = color >> 8
    r = color % 256
    return (r, g, b)


class Game:
    def __init__(self, title: str, size: Tuple[int, int], fps: int = 30):
        """
        初始化游戏类，包含标题、窗口大小和帧率。

        Args:
            title (str): 游戏窗口的标题。
            size (Tuple[int, int]): 窗口的尺寸（宽度，高度）。
            fps (int, optional): 游戏更新的每秒帧数。默认为30。
        """
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption(title)
        self.keys = {}
        self.keys_up = {}
        self.clicks = {}
        self.timer = pygame.time.Clock()
        self.fps = fps
        self.score = 0
        self.end = False
        self.fullscreen = False
        self.last_time = pygame.time.get_ticks()
        self.is_pause = False
        self.is_draw = True
        self.score_font = pygame.font.SysFont("Calibri", 130, True)

    def bind_key(self, key: int | list[int], action: Callable[[int], None]):
        """
        绑定一个函数到按键事件。

        Args:
            key (int | list[int]): 要绑定的单个按键或按键列表。
            action (Callable[[int], None]): 按键按下时调用的函数。
        """
        if isinstance(key, list):
            for k in key:
                self.keys[k] = action
        elif isinstance(key, int):
            self.keys[key] = action

    def bind_key_up(self, key: int | list[int], action: Callable[[int], None]):
        """
        绑定一个函数到按键释放事件。

        Args:
            key (int | list[int]): 要绑定的单个按键或按键列表。
            action (Callable[[int], None]): 按键释放时调用的函数。
        """
        if isinstance(key, list):
            for k in key:
                self.keys_up[k] = action
        elif isinstance(key, int):
            self.keys_up[key] = action

    def bind_click(self, button: int, action: Callable[[int, int], None]):
        """
        绑定一个函数到鼠标按钮点击事件。

        Args:
            button (int): 要绑定的鼠标按钮（1表示左键点击等）。
            action (Callable[[int, int], None]): 点击时调用的函数，Args为(x, y)。
        """
        self.clicks[button] = action

    def pause(self, key: int):
        """
        切换游戏的暂停状态。

        Args:
            key (int): 触发暂停动作的按键。
        """
        self.is_pause = not self.is_pause

    def set_fps(self, fps: int):
        """
        设置游戏的每秒帧数。

        Args:
            fps (int): 期望的每秒帧数。
        """
        self.fps = fps

    def handle_input(self, event: pygame.event.Event):
        """
        处理用户输入的按键和鼠标事件。

        Args:
            event (pygame.event.Event): 要处理的事件。
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys.keys():
                self.keys[event.key](event.key)
            if event.key == pygame.K_F11:  # F11键用于全屏
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.screen = pygame.display.set_mode(
                        self.size, pygame.FULLSCREEN, 32
                    )
                else:
                    self.screen = pygame.display.set_mode(self.size, 0, 32)
        if event.type == pygame.KEYUP:
            if event.key in self.keys_up.keys():
                self.keys_up[event.key](event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.clicks.keys():
                self.clicks[event.button](*event.pos)

    def run(self):
        """主游戏循环，处理事件、更新和绘制。"""
        while True:
            for event in pygame.event.get():
                self.handle_input(event)
            self.timer.tick(self.fps)

            self.update(pygame.time.get_ticks())
            self.draw(pygame.time.get_ticks())

    def draw_score(
        self, color: Tuple[int, int, int], rect: Optional[pygame.Rect] = None
    ):
        """
        在屏幕上绘制游戏分数。

        Args:
            color (Tuple[int, int, int]): 分数文本的颜色。
            rect (Optional[pygame.Rect], optional): 定位矩形。默认为None。
        """
        score = self.score_font.render(str(self.score), True, color)
        if rect is None:
            r = self.screen.get_rect()
            rect = score.get_rect(center=r.center)
        self.screen.blit(score, rect)

    def is_end(self) -> bool:
        """检查游戏是否结束。

        Returns:
            bool: 如果游戏结束返回True，否则返回False。
        """
        return self.end

    def update(self, current_time: int):
        """
        更新游戏状态。在子类中重写此方法以实现游戏特定逻辑。

        Args:
            current_time (int): 当前时间（毫秒）。
        """
        pass

    def draw(self, current_time: int):
        """
        绘制游戏元素。在子类中重写此方法以实现游戏特定视觉效果。

        Args:
            current_time (int): 当前时间（毫秒）。
        """
        pass


class Test(Game):
    def __init__(self, title: str, size: Tuple[int, int], fps: int = 30):
        """
        初始化测试游戏，包含特定的标题、窗口大小和帧率。

        Args:
            title (str): 游戏窗口的标题。
            size (Tuple[int, int]): 窗口的尺寸（宽度，高度）。
            fps (int, optional): 游戏更新的每秒帧数。默认为30。
        """
        super(Test, self).__init__(title, size, fps)
        self.bind_key(pygame.K_RETURN, self.press_enter)

    def press_enter(self):
        """处理Enter键按下事件。"""
        print("press enter")

    def draw(self, current_time: int):
        """绘制测试游戏的游戏元素。"""
        pass


def press_space(key: int):
    """处理空格键按下事件。"""
    print("press space.")


def click(x: int, y: int):
    """处理鼠标点击事件，打印点击的坐标。"""
    print(x, y)


def main():
    """
    主函数，初始化并运行一个测试游戏实例。
    包括示例按键和点击绑定。
    """
    print(hex2rgb(0x012456))
    game = Test("game", (640, 480))
    game.bind_key(pygame.K_SPACE, press_space)
    game.bind_click(1, click)
    game.run()


if __name__ == "__main__":
    main()

# 要创建可执行文件，请在终端中运行以下命令：
# pip install pyinstaller
# pyinstaller -F -w game.py
