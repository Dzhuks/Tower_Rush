from scripts.units import *
import sqlite3


class Tower(pygame.sprite.Sprite):
    def __init__(self, tower_id, x, y, *groups):
        super(Tower, self).__init__(*groups)

        self.con = sqlite3.connect(DATABASE)
        cur = self.con.cursor()

        self.whole_img = cur.execute(f"SELECT whole_img FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.whole_img = load_image(self.whole_img)

        self.broken_img = cur.execute(f"SELECT broken_img FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.broken_img = load_image(self.whole_img)

        self.max_hp = cur.execute(f"SELECT hp FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.cur_hp = self.max_hp

        self.image = self.whole_img
        self.rect = self.image.get_rect()
        self.rect.move(x, y)
        self.is_whole = True

    def defense(self, damage):
        self.cur_hp -= damage
        if self.cur_hp <= 0:
            self.is_whole = False

    def draw_health_bar(self, win):
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f"{self.cur_hp}/{self.max_hp}", True, ORANGE)
        win.blit(string_rendered, (win.get_width() - string_rendered.get_width(), 0))

    def is_broken(self):
        return not self.is_whole

    def update(self):
        if self.is_whole:
            self.image = self.whole_img
        else:
            self.image = self.broken_img
        self.draw_health_bar(self.image)


class EnemyTower(Tower):
    def spawn(self, name):
        EnemyUnit(name, self.rect.x + self.rect.width / 2, self.rect.y, ENEMIES_SPRITES)


class PlayerTower(Tower):
    def spawn(self, name):
        Unit(name, self.rect.x + self.rect.width / 2, self.rect.y, PLAYER_SPRITES)
