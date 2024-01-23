# Space Survival War
import pygame
import resources

from utils import draw_init, show_game_over
from config import FPS, WIDTH, HEIGHT
from game_state import GameState


# 遊戲初始化 and 創建視窗
pygame.init()
resources.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空生存戰")
clock = pygame.time.Clock()
game_state = GameState()


# 遊戲迴圈
show_init = True
running = True

while running:
    # 显示初始屏幕
    if show_init:
        close = draw_init(screen, clock)
        if close:
            break
        show_init = False

    # 处理输入
    running = game_state.process_input()
    if not running:
        break

    # 更新游戏状态
    game_state.update()

    # 渲染画面
    game_state.render(screen)

    # 检查游戏是否结束
    if game_state.check_game_over():
        show_game_over(screen)
        show_init = True
        game_state = GameState()  # 重置游戏状态

    # 更新屏幕显示
    pygame.display.update()

    # 控制游戏循环速率
    clock.tick(FPS)

pygame.quit()