import pygame
from scripts.menu import MainMenu
from scripts.start_screen import start_screen
from scripts.game_over import game_over
from scripts.constants import *


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    game_over(screen)
    # start_screen(screen)
    # main_menu = MainMenu()
    # main_menu.run(screen)
