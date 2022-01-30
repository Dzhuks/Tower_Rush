import sqlite3

from scripts.units import cut_sheet
from scripts.functions import *


# класс кнопки
class Button(pygame.sprite.Sprite):
    def __init__(self, name, img, x, y, *group):
        super(Button, self).__init__(*group)
        self.name = name  # название кнопки
        self.image = img  # изображение кнопки
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # функция проверяющий нажата ли кнопка
    def is_clicked(self, pos):
        return self.rect.collidepoint(*pos)


# кнопка покупки
class BuyButton(Button):
    def __init__(self, unit_name, cost, img, x, y, *group):
        super(BuyButton, self).__init__(unit_name, img, x, y, *group)
        self.cost = cost  # стоимость юнита

        # рисуем цену на изображение кнопки
        font = pygame.font.Font(None, 20)
        cost_text = font.render(f"{self.cost}$", True, WHITE)
        cost_text_x = self.image.get_width() - cost_text.get_width()
        cost_text_y = self.image.get_height() - cost_text.get_height()
        self.image.blit(cost_text, (cost_text_x, cost_text_y))
        rect = (0, 0, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(self.image, BLACK, rect, 1)

    # при нажатие вернуть имя кнопки и стоимость
    def clicked(self, pos):
        if self.is_clicked(pos):
            return self.name, self.cost


# кнопка включатель
class OnOffButton(Button):
    def __init__(self, name, pause_img, active_img, x, y, *group):
        super(OnOffButton, self).__init__(name, active_img, x, y, *group)
        self.pause_img = pause_img  # изображение пассивной кнопки
        self.active_img = active_img  # изображение активной кнопки
        self.pause = False

    # обновляем кнопку
    def update(self, *args, **kwargs) -> None:
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            self.clicked(args[0].pos)

        # изменить изображение в зависимости от self.pause
        if self.pause:
            self.image = self.pause_img
        else:
            self.image = self.active_img

    # функция заглушка для наследников
    def clicked(self, pos):
        pass


# кнопка паузы
class PauseButton(OnOffButton):
    # изображение пассивной и активной кнопки
    pause_img = load_image("icons\\pause_button.png")
    active_img = load_image("icons\\resume_button.png")

    def __init__(self, name, x, y, *group):
        super(PauseButton, self).__init__(name, PauseButton.pause_img, PauseButton.active_img, x, y, *group)

    # функция нажатие на кнопку
    def clicked(self, pos):
        if self.is_clicked(pos):
            self.pause = not self.pause


# кнопка остановки музыки
class SoundOnButton(OnOffButton):
    # изображение пассивной и активной кнопки
    pause_img = load_image("icons\\sound_off_icon.png")
    active_img = load_image("icons\\sound_on_icon.png")

    def __init__(self, name, x, y, *group):
        super(SoundOnButton, self).__init__(name, SoundOnButton.pause_img, SoundOnButton.active_img, x, y, *group)

    # функция нажатие на кнопку
    def clicked(self, pos):
        if self.is_clicked(pos):
            self.pause = not self.pause
            if self.pause:
                pygame.mixer.music.pause()  # остановить музыку
            else:
                pygame.mixer.music.unpause()  # продолжить музыку


# класс меню
class Menu:
    def __init__(self, img: pygame.Surface, x, y):
        self.bg = img
        self.rect = pygame.Rect(x, y, *self.bg.get_size())
        self.buttons = pygame.sprite.Group()

    def draw(self, window: pygame.Surface):
        window.blit(self.bg, self.rect.topleft)
        self.buttons.draw(window)


# класс покупки меню
class BuyMenu(Menu):
    def __init__(self):
        super(BuyMenu, self).__init__(load_image("backgrounds\\buy_menu.png"), 0, 0)
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.con = sqlite3.connect(DATABASE)
        self.add_units()

    # функция добавления юнита
    def add_unit(self, unit_name, cost):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        # иконка юнита
        animation = load_image(cur.execute(f"SELECT animation FROM units WHERE name=\"{unit_name}\"").fetchall()[0][0])
        rows, columns = cur.execute(f"SELECT rows, columns FROM units WHERE name=\"{unit_name}\"").fetchall()[0]
        unit_img = cut_sheet(animation, rows, columns)[0]

        # вычисляем координаты кнопки
        btn_size = btn_width, btn_height = 90, 50
        btn_img = pygame.transform.scale(unit_img, btn_size)
        btn_x = self.rect.x + (btn_width + 10) * len(self.buttons.sprites())
        btn_y = self.rect.y + self.rect.height - btn_height
        BuyButton(unit_name, cost, btn_img, btn_x, btn_y, self.buttons)

    # при нажатие на меню, вернуть имя и стоимость юнита
    def get_clicked(self, pos):
        for btn in self.buttons.sprites():
            if btn.clicked(pos) is not None:
                return btn.clicked(pos)

        return None

    # функция добавления юнитов
    def add_units(self):
        # получаем из базы данных юниты игрока
        cur = self.con.cursor()
        que = """
        SELECT name FROM units 
            WHERE type_id=(SELECT type_id FROM types WHERE type="player")
        """
        units = cur.execute(que).fetchall()

        # добавляем юнитов
        for unit in units:
            unit = unit[0]
            que = f"SELECT cost FROM units WHERE name=\"{unit}\""
            cost = cur.execute(que).fetchall()[0][0]
            self.add_unit(unit, cost)
