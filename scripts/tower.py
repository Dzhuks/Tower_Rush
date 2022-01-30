from scripts.units import *
from scripts.functions import *


# класс башни игрока
class PlayerTower(pygame.sprite.Sprite):

    def __init__(self, tower_id, *groups):
        super(PlayerTower, self).__init__(*groups)

        self.con = sqlite3.connect(DATABASE)
        cur = self.con.cursor()

        # получаем изображение башни
        self.whole_img = cur.execute(f"SELECT whole_img FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.whole_img = load_image(f"sprites\\towers\\{self.whole_img}")

        # звуки разрущения и повреждения башни
        self.broke_sound = load_sound("hammer-hit-break-windshield_gk8u8pn_.mp3")
        self.destruction_sound = load_sound("GTA Wasted (Потрачено)_1ao1.mp3")

        # максимальное хп и текущее зп
        self.max_hp = cur.execute(f"SELECT hp FROM towers WHERE tower_id={tower_id}").fetchall()[0][0]
        self.cur_hp = self.max_hp

        # перемешаем башню
        self.image = self.whole_img
        self.rect = self.image.get_rect()
        self.rect.x = BATTLEFIELD_WIDTH - self.rect.width
        self.rect.y = BATTLEFIELD_HEIGHT - self.rect.height

        self.is_whole = True  # функция отслеживания целостности башни

    # функция получения урона
    def defense(self, damage):
        # если башня ращрушена издать звук разрушения, иначе звук повреждения
        if self.cur_hp > 0 >= self.cur_hp - damage:
            self.is_whole = False
            self.destruction_sound.play()
        else:
            self.broke_sound.play()
        # уменьшить текущее здоровье
        self.cur_hp -= damage

    # функция рисование текущего и максимального здоровья
    def draw_health_bar(self, win):
        font = pygame.font.Font(None, 15)
        string_rendered = font.render(f"{self.cur_hp}/{self.max_hp}", True, ORANGE)
        win.blit(string_rendered, (self.rect.width - string_rendered.get_width(), 0))
        return win

    # вернуть цела ли башня
    def is_broken(self):
        return not self.is_whole

    # функция обновления
    def update(self):
        if self.is_whole:
            self.image = self.whole_img
        self.image = self.draw_health_bar(self.image.copy())

    # функция спавна юнита
    def spawn(self, name):
        Unit(name, self, PLAYER_SPRITES, ALL_SPRITES)


# класс вражеской башни
class EnemyTower(PlayerTower):
    def __init__(self, tower_id, *groups):
        super(EnemyTower, self).__init__(tower_id, *groups)
        self.rect.x = 0
        # для вражеской башни изменить звук разрушения
        self.destruction_sound = load_sound("odinochnyj-hlopok-vzryv.mp3")

    # переопределяем функцию спавн
    def spawn(self, name):
        cur = self.con.cursor()
        type_id = cur.execute(f"SELECT type_id FROM units WHERE name=\"{name}\"").fetchall()[0][0]
        boss_id = cur.execute(f"SELECT type_id FROM types WHERE type=\"boss\"").fetchall()[0][0]
        # если type_id равен id босс, то призвать босса, иначе вражеского юнита
        if type_id == boss_id:
            Boss(name, self, ENEMIES_SPRITES, ALL_SPRITES)
        else:
            EnemyUnit(name, self, ENEMIES_SPRITES, ALL_SPRITES)

    def get_money(self):
        return 0
