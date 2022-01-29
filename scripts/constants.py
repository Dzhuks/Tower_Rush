import pygame
import sys
import os


pygame.init()
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
BATTLEFIELD_SIZE = BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT - 75
screen = pygame.display.set_mode(SCREEN_SIZE)

FPS = 60
GRAVITY = 1

DATABASE = "data\\stats_db.db"

ALL_SPRITES = pygame.sprite.Group()
ENEMIES_SPRITES = pygame.sprite.Group()
PLAYER_SPRITES = pygame.sprite.Group()

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
ORANGE = pygame.Color(255, 165, 0)
BLOOD_RED = pygame.Color(102, 0, 0)
DARK_GREEN = pygame.Color(23, 114, 69)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_sound(name):
    fullname = os.path.join('data', 'sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        terminate()
    return pygame.mixer.Sound(fullname)


def load_font(name, size=30):
    fullname = os.path.join('data', 'fonts', name)
    if not os.path.isfile(fullname):
        print(f"Файл с шрифтом '{fullname}' не найден")
        terminate()
    return pygame.font.Font(fullname, size)


def clear_sprites():  # Очистка спрайтов
    ALL_SPRITES.empty()
    PLAYER_SPRITES.empty()
    ENEMIES_SPRITES.empty()
