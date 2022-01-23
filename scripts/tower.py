import pygame
from units import *


class Tower(pygame.sprite.Sprite):
    def __init__(self, whole_img, broken_img, hp, x, y):
        super(Tower, self).__init__()
        self.whole_img = whole_img
        self.broken_img = broken_img
        self.image = self.whole_img
        self.max_hp = hp
        self.cur_hp = hp
        self.rect = self.image.get_rect()
        self.rect.move(x, y)
        self.is_alive = True

    def attacked(self, damage):
        self.cur_hp -= damage
        if self.cur_hp <= 0:
            self.is_alive = False

    def update(self):
        if self.is_alive:
            self.image = self.whole_img
        else:
            self.image = self.broken_img
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f"{self.cur_hp}/{self.max_hp}", True, (255, 165, 0))
        self.image.blit(string_rendered, (self.image.get_width() - string_rendered.get_width(), 0))


class EnemyTower(Tower):
    def spawn(self, name):
        unit = EnemyUnit(name, self.rect.x + self.rect.width / 2, self.rect.y)
        ENEMIES_SPRITES.add(unit)


class PlayerTower(Tower):
    def spawn(self, name):
        unit = PlayerUnit(name, self.rect.x + self.rect.width / 2, self.rect.y)
        PLAYER_SPRITES.add(unit)
