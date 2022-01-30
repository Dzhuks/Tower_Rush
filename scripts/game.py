import time
import csv

from scripts.menu import BuyMenu, PauseButton, SoundOnButton
from scripts.tower import *
from scripts.end_game import *
from scripts.credits import *


class Game:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE)
        self.money = 0
        self.pause = False
        self.music_pause = False

        self.menu = BuyMenu()
        self.add_units()

        self.buttons = pygame.sprite.Group()
        self.pause_button = PauseButton("pause_button", 0, 0, self.buttons, ALL_SPRITES)
        self.sound_on_off = SoundOnButton("sound_on_off", 50, 0, self.buttons, ALL_SPRITES)

        self.cur_level = save.last_save()
        if self.cur_level is None:
            self.cur_level = 1
        self.render_level()
        self.levels = {}
        self.render_enemies()
        self.iteration = 0
        self.start_time = time.time()  # время начало игры
        self.killed_enemies = 0

    def zeroing_out(self):
        clear_sprites()
        self.money = 0
        self.iteration = 0
        self.start_time = time.time()  # время начало игры
        self.killed_enemies = 0

    def save_progress(self, status):
        level = self.cur_level
        period = convert_time_to_string(time.time() - self.start_time)
        killed_enemies = self.killed_enemies
        tower_hp = self.player_tower.cur_hp
        save.save(level, period, killed_enemies, tower_hp, status)

    def render_level(self):
        self.zeroing_out()

        cur = self.con.cursor()
        que = f"""
        SELECT level_name, bg, background_music, enemy_tower_id, player_tower_id FROM levels 
            WHERE level_number={self.cur_level}"""
        result = cur.execute(que).fetchall()
        if not result:
            self.cur_level -= 1
            self.save_progress("win")
            end_screen()
            return

        level_name, background, background_music, enemy_tower_id, player_tower_id = result[0]
        self.level_name = level_name
        self.bg = load_image(background)
        self.enemy_tower = EnemyTower(enemy_tower_id, ENEMIES_SPRITES, ALL_SPRITES)
        self.player_tower = PlayerTower(player_tower_id, PLAYER_SPRITES, ALL_SPRITES)
        play_background_music(background_music, self.music_pause)
        ALL_SPRITES.add(self.pause_button)

    def add_units(self):
        cur = self.con.cursor()
        que = """SELECT name FROM units 
    WHERE type_id=(SELECT type_id FROM types WHERE type="player")"""
        units = cur.execute(que).fetchall()
        for unit in units:
            unit = unit[0]
            que = f"SELECT cost FROM units WHERE name=\"{unit}\""
            cost = cur.execute(que).fetchall()[0][0]
            self.menu.add_unit(unit, cost)

    def spawn(self, name, cost):
        if self.money >= cost:
            self.money -= cost
            self.player_tower.spawn(name)

    def gen_enemies(self):
        enemies = self.levels[self.cur_level]
        for enemy in enemies.keys():
            spawn_time, frequency = enemies[enemy]
            spawn_time *= FPS
            if self.iteration == spawn_time:
                self.enemy_tower.spawn(enemy)
            if self.iteration > spawn_time and frequency != -1:
                frequency *= FPS
                if self.iteration % frequency == 0:
                    self.enemy_tower.spawn(enemy)

    def draw_money_string(self, win):
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f"{self.money}$", True, DARK_GREEN)
        win.blit(string_rendered, (win.get_width() - string_rendered.get_width(), 0))

    def draw(self, win):
        win.fill(BLACK)
        win.blit(self.bg, (0, 0))

        ALL_SPRITES.draw(win)
        ENEMIES_SPRITES.draw(win)
        PLAYER_SPRITES.draw(win)

        self.menu.draw(win)

        self.draw_money_string(win)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(self.level_name, True, ORANGE)
        win.blit(string_rendered, (win.get_width() / 2 - string_rendered.get_width() / 2, 0))

        self.buttons.draw(win)

    def run(self, window):
        running = True
        clock = pygame.time.Clock()

        while running:
            if self.pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.buttons.update(event)
                        self.pause = self.pause_button.pause
                        self.music_pause = self.sound_on_off.pause
            else:
                self.iteration += 1
                if self.iteration % 3 == 0:
                    self.money += 100
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu.get_clicked(event.pos) is not None:
                            self.spawn(*self.menu.get_clicked(event.pos))
                        else:
                            self.buttons.update(event)
                            self.pause = self.pause_button.pause
                            self.music_pause = self.sound_on_off.pause
                if not self.enemy_tower.is_whole:
                    self.save_progress("win")
                    self.cur_level += 1
                    win()
                    self.render_level()

                if not self.player_tower.is_whole:
                    self.save_progress("lose")
                    game_over()
                    running = False
                self.gen_enemies()

                ALL_SPRITES.update()
                for sprite in ENEMIES_SPRITES.sprites():
                    self.money += sprite.get_money()
                self.draw(window)

            clock.tick(FPS)
            pygame.display.flip()

    def render_enemies(self):
        with open("data\\levels.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            next(reader)
            for item in reader:
                self.levels[int(item[0])] = {}
                for i in item[1:]:
                    name, value = i.split(":")
                    time, delta = map(int, value[1:-1].split(", "))
                    self.levels[int(item[0])][name] = (time, delta)
