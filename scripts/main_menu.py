import pygame
import os
import sys
from scripts.game import Game


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


class MainMenu:
    def __init__(self, win: pygame.Surface):
        self.win = win
        self.width, self.height = self.win.get_size()
        self.bg = load_image('main_menu\\bg.png')
        self.bg = pygame.transform.scale(self.bg, self.win.get_size())

        self.logo = load_image('main_menu\\logo.png')

        self.start_btn = load_image('main_menu\\start_button.png')
        self.start_btn_x = self.width / 2 - self.start_btn.get_width() / 2
        self.start_btn_y = 150

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()

                    if self.start_btn_x <= x <= self.start_btn_x + self.start_btn.get_width():
                        if self.start_btn_y <= y <= self.start_btn_y + self.start_btn.get_height():
                            game = Game(self.win)
                            game.run()
                            del game
                            running = False

            self.win.fill(pygame.color.Color("black"))
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        self.win.blit(self.logo, (self.width / 2 - self.logo.get_width() / 2, 0))
        self.win.blit(self.start_btn, (self.start_btn_x, self.start_btn_y))
