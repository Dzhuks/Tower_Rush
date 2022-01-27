import pygame
import sqlite3
from scripts.menu import *
from scripts.tower import *


class Game:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE)
        self.money = 0

        self.menu = BuyMenu(load_image(""), 0, SCREEN_HEIGHT - 100)
        self.add_units()

        self.cur_level = 1
        self.levels = {}
        self.render_level()
        self.pause_button = PauseButton("pause_button", load_image(""), load_image(""), 550, 0, ALL_SPRITES)

    def render_level(self):
        cur = self.con.cursor()
        que = f"""
        SELECT bg, enemy_tower_id, player_tower_id FROM levels 
            WHERE level_number={self.cur_level}"""
        result = cur.execute(que).fetchall()[0]
        self.bg = result[0]

        enemy_tower_id = result[1]
        player_tower_id = result[2]

        self.enemy_tower = EnemyTower(enemy_tower_id, 0, 200, TOWER_SPRITES)
        self.player_tower = PlayerTower(player_tower_id, 600, 200, TOWER_SPRITES)

    def add_units(self):
        cur = self.con.cursor()
        units = ["cool_doge", "dababy", "nyan_cat", "pop_cat", "uganda_knucles"]
        for unit in units:
            unit_img, cost = cur.execute(f"SELECT image, cost FROM units WHERE name={unit}").fetchall()[0]
            self.menu.add_button(unit, cost, unit_img)

    def spawn(self, name, cost):
        if self.money >= cost:
            self.money -= cost
            self.player_tower.spawn(name)

    def gen_enemies(self, frames):
        enemies = self.levels[self.cur_level]
        for enemy in enemies.keys():
            time = enemies[enemy]
            if frames % time == 0:
                self.enemy_tower.spawn(enemy)

    def draw_money_string(self, win):
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f"{self.money}$", True, ORANGE)
        win.blit(string_rendered, (win.get_width() - string_rendered.get_width(), 25))

    def run(self, win):
        running = True
        paused = False
        clock = pygame.time.Clock()
        iteration = 0
        while running:
            iteration += 1
            if paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_button.is_clicked(event.pos):
                            self.pause_button.clicked(event)
                            paused = self.pause_button.pause
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu.get_clicked(event.pos) is not None:
                            self.spawn(*self.menu.get_clicked(event.pos))
                        elif self.pause_button.is_clicked(event.pos):
                            self.pause_button.clicked(event)
                            paused = self.pause_button.pause
                self.gen_enemies(iteration)
                win.fill(pygame.Color('black'))
                ALL_SPRITES.draw(win)
                TOWER_SPRITES.draw(win)
                ENEMIES_SPRITES.draw(win)
                PLAYER_SPRITES.draw(win)
                self.menu.draw(win)
            clock.tick(FPS)
            pygame.display.flip()
