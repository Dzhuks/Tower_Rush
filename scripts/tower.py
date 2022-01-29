from scripts.units import *


class PlayerTower(pygame.sprite.Sprite):
    def __init__(self, tower_id, *groups):
        super(PlayerTower, self).__init__(*groups)

        self.con = sqlite3.connect(DATABASE)
        cur = self.con.cursor()

        self.whole_img = cur.execute(f"SELECT whole_img FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.whole_img = load_image(f"sprites\\towers\\{self.whole_img}")

        self.broken_img = cur.execute(f"SELECT broken_img FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.broken_img = load_image(f"sprites\\towers\\{self.broken_img}")

        self.max_hp = cur.execute(f"SELECT hp FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.cur_hp = self.max_hp

        self.image = self.whole_img
        self.rect = self.image.get_rect()
        self.rect.x = BATTLEFIELD_WIDTH - self.rect.width
        self.rect.y = BATTLEFIELD_HEIGHT - self.rect.height
        self.is_whole = True

    def defense(self, damage):
        print(self.cur_hp)
        self.cur_hp -= damage
        if self.cur_hp <= 0:
            self.is_whole = False

    def draw_health_bar(self, win):
        font = pygame.font.Font(None, 15)
        string_rendered = font.render(f"{self.cur_hp}/{self.max_hp}", True, DARK_GREEN)
        win.blit(string_rendered, (self.rect.width - string_rendered.get_width(), 0))
        return win

    def is_broken(self):
        return not self.is_whole

    def update(self):
        if self.is_whole:
            self.image = self.whole_img
        else:
            self.image = self.broken_img
        self.image = self.draw_health_bar(self.image.copy())

    def spawn(self, name):
        Unit(name, self, PLAYER_SPRITES, ALL_SPRITES)


class EnemyTower(PlayerTower):
    def __init__(self, tower_id, *groups):
        super(EnemyTower, self).__init__(tower_id, *groups)
        self.rect.x = 0

    def spawn(self, name):
        EnemyUnit(name, self, ENEMIES_SPRITES, ALL_SPRITES)

    def get_money(self):
        return 0
