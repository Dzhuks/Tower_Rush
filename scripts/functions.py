import sys
import os
from scripts.constants import *


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
    fullname = os.path.join('data', "audio", 'sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        terminate()
    return pygame.mixer.Sound(fullname)


def play_background_music(name, paused=False):
    print(paused)
    fullname = os.path.join('data', "audio", "background music", name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        terminate()
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.set_volume(0.4)
    if not paused:
        pygame.mixer.music.play(-1)


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


def convert_time_to_string(time):
    time_difference = int(time)
    minutes = time_difference // 60
    seconds = time_difference % 60
    return f"{minutes}:{seconds}"