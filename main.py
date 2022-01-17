from scripts.main_menu import MainMenu
import pygame


SIZE = WIDTH, HEIGHT = 600, 400


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode(SIZE)
    main_menu = MainMenu(win)
    main_menu.run()
