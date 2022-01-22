from scripts.main_menu import MainMenu
from scripts.constants import *
import pygame
import os
import sys


BLACK = pygame.Color('black')

pygame.init()
screen = pygame.display.set_mode(SIZE)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["Котики, Люди, Школьники",
                  "Когда-то давно все они жили в мире, но все изменилось когда Поносенко всех переиграл и уничтожил",
                  "Только Амогус властелин всех мемов и рофлов мог остановить войну.",
                  "Но когда мир нуждался в амогусе больше всего он исчез.",
                  "Прошло десять лет и появился новый Амогус под именем Кличко, ",
                  "и хотя его искусство завтрашнего дня и арифметики было велико ему пристояло еще многому научится.",
                  "Но я верила что Кличко спасет мир."]

    fon = pygame.transform.scale(load_image('main_menu\\bg.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    main_menu = MainMenu(screen)
    main_menu.run()
