# 五子棋游戏

欢迎来到五子棋，这是一个双人游戏，目标是在17x17的棋盘上放置五个连续的相同颜色（黑色或白色）的棋子。该项目使用Pygame创建了一个互动且引人入胜的体验。

## 功能
- 17x17的网格棋盘。
- 双人轮流游戏（黑白棋子）。
- 自动检测任意方向的五连胜。
- 高亮显示获胜的棋子序列。

## 入门指南

### 先决条件

- **Python 3.8+**
- **Pygame库**

安装Pygame，请使用：

（Windows）
```
pip install pygame
```
（macOS/Linux）
```
pip3 install pygame
```

### 安装

1. 克隆仓库：
   ```
   git clone https://github.com/PythonDeveloper29042/GomokuGame_zh_CN.git
   ```
2. 进入项目目录：
   ```
   cd GomokuGame
   ```
3. 运行游戏：
   ```
   python main.py
   ```

### 创建可执行文件（可选）
您可以使用`pyinstaller`创建一个独立的可执行文件：

```
pip install pyinstaller
pyinstaller -F -w main.py
```

这将在`dist`目录中生成一个可执行文件。

如果您使用的是macOS和Linux，请将`pip`替换为`pip3`。

## 游戏说明

1. **目标**：放置五个连续的棋子（水平、垂直或对角线）以获胜。
2. **控制**：使用鼠标左键在棋盘上放置棋子。
3. **胜利条件**：当玩家达成五连胜时，游戏会显示获胜消息并高亮显示获胜的棋子序列。

## 代码结构

- **`main.py`**：包含主要的游戏逻辑、棋盘绘制、棋子放置和胜利检测机制。
- **`game.py`**：基础游戏类，管理Pygame设置和基本功能。

## 类概述

### `Gomoku`
继承自`game.Game`，包括：
- `click(x: int, y: int)`: 处理棋子放置和轮流变化。
- `check_win() -> list[tuple[int, int]] | None`: 检查棋盘上的获胜序列。
- `check_chess(i: int, j: int) -> list[tuple[int, int]] | None`: 检查指定方向的连续棋子。
- `draw_chess(color: tuple[int, int, int], i: int, j: int)`: 在指定的棋盘位置绘制棋子。
- `draw_board()`: 初始化带有网格线和中心点的棋盘。

## 自定义

您可以修改`main.py`中的`ROWS`和`SIDE`常量来改变棋盘大小和网格间距。

## 鸣谢

- **作者**：PythonDeveloper29042
- **联系**：[pythondeveloper.29042@outlook.com](mailto:pythondeveloper.29042@outlook.com)
