import pygame.display
from scripts.credits import *
from scripts.main_menu import MainMenu
from scripts.constants import *


if __name__ == '__main__':
    pygame.display.set_caption("Meme Rush")
    if save.last_save() is None:
        start_screen()
    main_menu = MainMenu()
    main_menu.run(screen)

