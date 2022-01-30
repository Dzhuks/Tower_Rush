import sys
import os

import pygame.mixer
from scripts.constants import *


# инициализация pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()


# функция для завершения игры
def terminate():
    pygame.quit()
    sys.exit()


# функция загрузки изображения
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


# функция загрузки звука
def load_sound(name):
    fullname = os.path.join('data', "audio", 'sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        terminate()
    sound = pygame.mixer.Sound(fullname)
    sound.set_volume(VOLUME)
    return sound


# функция загрузки фоновой музыки
def play_background_music(name, paused=False):
    fullname = os.path.join('data', "audio", "background music", name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        terminate()
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.set_volume(VOLUME)
    if not paused:  # если нажата пауза, то не играть
        pygame.mixer.music.play(-1)


# функция загрузки шрифта
def load_font(name, size=30):
    fullname = os.path.join('data', 'fonts', name)
    if not os.path.isfile(fullname):
        print(f"Файл с шрифтом '{fullname}' не найден")
        terminate()
    return pygame.font.Font(fullname, size)


# функция очистки групп спрайтов
def clear_sprites():
    ALL_SPRITES.empty()
    PLAYER_SPRITES.empty()
    ENEMIES_SPRITES.empty()


# конвертирование времени в формат hh:mm
def convert_time_to_string(time):
    time_difference = int(time)
    minutes = time_difference // 60
    seconds = time_difference % 60
    return f"{minutes}:{seconds}"