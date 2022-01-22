import pygame
import sqlite3


class Game:
    def __init__(self, win):
        self.con = sqlite3.connect("data\\stats_db.db")
        self.win = win
        self.enemies = pygame.sprite.Group()
        self.player_units = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.cur_level = 1
        self.levels = {}
        self.render_level()

    def render_level(self):
        cur = self.con.cursor()
        que = "SELECT "

    def run(self):
        pass