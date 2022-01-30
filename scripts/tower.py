from scripts.units import *
from scripts.functions import *


class PlayerTower(pygame.sprite.Sprite):

    def __init__(self, tower_id, *groups):
        super(PlayerTower, self).__init__(*groups)

        self.con = sqlite3.connect(DATABASE)
        cur = self.con.cursor()

        self.whole_img = cur.execute(f"SELECT whole_img FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.whole_img = load_image(f"sprites\\towers\\{self.whole_img}")

        self.broke_sound = load_sound("hammer-hit-break-windshield_gk8u8pn_.mp3")
        self.destruction_sound = load_sound("GTA Wasted (Потрачено)_1ao1.mp3")

        self.max_hp = cur.execute(f"SELECT hp FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.cur_hp = self.max_hp

        self.image = self.whole_img
        self.rect = self.image.get_rect()
        self.rect.x = BATTLEFIELD_WIDTH - self.rect.width
        self.rect.y = BATTLEFIELD_HEIGHT - self.rect.height
        self.is_whole = True

    def defense(self, damage):
        if self.cur_hp > 0 >= self.cur_hp - damage:
            self.is_whole = False
            self.destruction_sound.play()
        else:
            self.broke_sound.play()
        self.cur_hp -= damage

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
        self.image = self.draw_health_bar(self.image.copy())

    def spawn(self, name):
        Unit(name, self, PLAYER_SPRITES, ALL_SPRITES)


class EnemyTower(PlayerTower):
    def __init__(self, tower_id, *groups):
        super(EnemyTower, self).__init__(tower_id, *groups)
        self.rect.x = 0
        self.destruction_sound = load_sound("odinochnyj-hlopok-vzryv.mp3")

    def spawn(self, name):
        cur = self.con.cursor()
        type_id = cur.execute(f"SELECT type_id FROM units WHERE name=\"{name}\"").fetchall()[0][0]
        boss_id = cur.execute(f"SELECT type_id FROM types WHERE type=\"boss\"").fetchall()[0][0]
        if type_id == boss_id:
            Boss(name, self, ENEMIES_SPRITES, ALL_SPRITES)
        else:
            EnemyUnit(name, self, ENEMIES_SPRITES, ALL_SPRITES)

    def get_money(self):
        return 0
