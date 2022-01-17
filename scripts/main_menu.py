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


class Button(pygame.sprite.Sprite):
    def __init__(self, img, x, y, *group):
        super().__init__(*group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_collided(self, pos) -> True:
        return self.rect.collidepoint(*pos)

    def hover(self):
        pass

    def active(self):
        pass

    def clicked(self):
        pass

    def update(self, *args) -> None:
        if args:
            if args[0].type == pygame.MOUSEMOTION and self.is_collided(args[0].pos):
                self.hover()

            elif args[0].type == pygame.MOUSEBUTTONDOWN and self.is_collided(args[0].pos):
                self.active()

            elif args[0].type == pygame.MOUSEBUTTONUP and self.is_collided(args[0].pos):
                self.clicked()


class MainMenu:
    def __init__(self, win: pygame.Surface):
        self.bg_img = load_image("main_menu\\bg.png")
        self.bg = pygame.transform.scale(self.bg_img, win.get_size())

        self.buttons = pygame.sprite.Group()
        self.start_btn_img = load_image("main_menu\\start_button.png")
        self.start_btn = Button(self.start_btn_img, win.get_width() / 2 - self.start_btn_img.get_width() / 2,
                                win.get_height() / 2 - self.start_btn_img.get_height() / 2, self.buttons)
        self.win = win

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.buttons.update(event)
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x1, y1 = pygame.mouse.get_pos()
                    x2, y2 = self.start_btn.rect.topleft
                    width, height = self.start_btn.rect.size

                    if x2 <= x1 <= x2 + width and y2 <= y1 <= y2 + height:
                        game = Game(self.win)
                        game.run()
                        del game

            self.draw()

            pygame.display.flip()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        self.buttons.draw(self.win)
