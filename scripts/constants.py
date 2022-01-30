import pygame
from scripts.save import Save


# размеры окна, поле битвы и создание окна
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
BATTLEFIELD_SIZE = BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT - 75
screen = pygame.display.set_mode(SCREEN_SIZE)

# константы
FPS = 60
GRAVITY = 1
VOLUME = 0.05
DATABASE = "data\\stats_db.db"

# сохранение
save = Save(DATABASE)

# группы спрайтов
ALL_SPRITES = pygame.sprite.Group()
ENEMIES_SPRITES = pygame.sprite.Group()
PLAYER_SPRITES = pygame.sprite.Group()
DEAD_SPRITES = pygame.sprite.Group()

# цвета
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
ORANGE = pygame.Color(255, 165, 0)
BLOOD_RED = pygame.Color(102, 0, 0)
DARK_GREEN = pygame.Color(23, 114, 69)