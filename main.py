from scripts.constants import *
from scripts.start_screen import start_screen
from scripts.main_menu import MainMenu


if __name__ == '__main__':
    pygame.init()
    start_screen(screen)
    main_menu = MainMenu()
    main_menu.run(screen)
