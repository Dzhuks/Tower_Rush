from scripts.menu import BuyMenu, PauseButton
from scripts.tower import *
from scripts.game_over import game_over


class Game:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE)
        self.money = 0

        self.menu = BuyMenu()
        self.add_units()

        self.buttons = pygame.sprite.Group()
        self.pause_button = PauseButton("pause_button", 0, 0, self.buttons, ALL_SPRITES)

        self.cur_level = 1
        self.levels = {1: {"trollface": (5, 20)}, 2: {}, 3: {}}
        self.render_level()
        self.iteration = 0

    def zeroing_out(self):
        clear_sprites()
        self.money = 0
        self.iteration = 0

    def render_level(self):
        self.zeroing_out()

        cur = self.con.cursor()
        que = f"""
        SELECT level_name, bg, enemy_tower_id, player_tower_id FROM levels 
            WHERE level_number={self.cur_level}"""
        result = cur.execute(que).fetchall()[0]
        if not result:
            self.win()
            return

        level_name, background, enemy_tower_id, player_tower_id = result
        self.level_name = level_name
        self.bg = load_image(background)
        self.enemy_tower = EnemyTower(enemy_tower_id, ENEMIES_SPRITES, ALL_SPRITES)
        self.player_tower = PlayerTower(player_tower_id, PLAYER_SPRITES, ALL_SPRITES)
        ALL_SPRITES.add(self.pause_button)

    def add_units(self):
        cur = self.con.cursor()
        que = """SELECT name FROM units 
    WHERE side=(SELECT side_id FROM sides WHERE side="player")"""
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
            frequency *= FPS
            if self.iteration == spawn_time:
                self.enemy_tower.spawn(enemy)
            if self.iteration > spawn_time:
                if self.iteration % frequency == 0:
                    self.enemy_tower.spawn(enemy)

    def draw_money_string(self, win):
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f"{self.money}$", True, DARK_GREEN)
        win.blit(string_rendered, (win.get_width() - string_rendered.get_width(), 0))

    def draw(self, win):
        win.fill(pygame.Color('black'))
        win.blit(self.bg, (0, 0))

        ALL_SPRITES.draw(win)
        ENEMIES_SPRITES.draw(win)
        PLAYER_SPRITES.draw(win)

        self.menu.draw(win)

        self.draw_money_string(win)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(self.level_name, True, ORANGE)
        win.blit(string_rendered, (win.get_width() / 2 - string_rendered.get_width() / 2, 0))

    def run(self, win):
        running = True
        paused = False
        clock = pygame.time.Clock()
        while running:
            if paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_button.is_clicked(event.pos):
                            self.pause_button.clicked(event.pos)
                            paused = self.pause_button.pause
            else:
                self.iteration += 1
                if self.iteration % 3 == 0:
                    self.money += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu.get_clicked(event.pos) is not None:
                            self.spawn(*self.menu.get_clicked(event.pos))
                        elif self.pause_button.is_clicked(event.pos):
                            self.pause_button.clicked(event.pos)
                            paused = self.pause_button.pause
                if not self.enemy_tower.is_whole:
                    self.cur_level += 1
                    self.render_level()

                if not self.player_tower.is_whole:
                    game_over(win)
                    running = False
                self.gen_enemies()

                ALL_SPRITES.update()
                for sprite in ENEMIES_SPRITES.sprites():
                    self.money += sprite.get_money()
                self.draw(win)

            clock.tick(FPS)
            pygame.display.flip()
