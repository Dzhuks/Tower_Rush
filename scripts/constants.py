import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 400
FPS = 60
CLOCK = pygame.time.Clock()
ALL_SPRITES = pygame.sprite.Group()
ENEMIES_SPRITES = pygame.sprite.Group()
PLAYER_SPRITES = pygame.sprite.Group()
TOWER_SPRITES = pygame.sprite.Group()

BLACK = pygame.Color("black")
ORANGE = pygame.Color(255, 165, 0)