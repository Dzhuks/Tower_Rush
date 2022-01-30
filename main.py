from scripts.credits import *
from scripts.main_menu import MainMenu
from scripts.constants import *

if __name__ == '__main__':
    pygame.init()
    start_screen(screen)
    main_menu = MainMenu()
    main_menu.run(screen)
