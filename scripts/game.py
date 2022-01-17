import pygame


class Game:
    def __init__(self, win):
        self.win = win
        self.cur_level = 1
        self.levels = {}
        self.enemies = pygame.sprite.Group()
        self.player_units = pygame.sprite.Group()

    def run(self):
        pass