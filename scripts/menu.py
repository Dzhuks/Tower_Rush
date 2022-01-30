import sqlite3

from scripts.constants import *
from scripts.units import cut_sheet


class Button(pygame.sprite.Sprite):
    def __init__(self, name, img, x, y, *group):
        super(Button, self).__init__(*group)
        self.name = name
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_clicked(self, pos):
        return self.rect.collidepoint(*pos)


class BuyButton(Button):
    def __init__(self, unit_name, cost, img, x, y, *group):
        super(BuyButton, self).__init__(unit_name, img, x, y, *group)
        self.cost = cost
        font = pygame.font.Font(None, 20)
        cost_text = font.render(f"{self.cost}$", True, WHITE)
        cost_text_x = self.image.get_width() - cost_text.get_width()
        cost_text_y = self.image.get_height() - cost_text.get_height()
        self.image.blit(cost_text, (cost_text_x, cost_text_y))
        rect = (0, 0, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(self.image, BLACK, rect, 1)

    def clicked(self, pos):
        if self.is_clicked(pos):
            return self.name, self.cost


class OnOffButton(Button):
    def __init__(self, name, pause_img, active_img, x, y, *group):
        super(OnOffButton, self).__init__(name, active_img, x, y, *group)
        self.pause_img = pause_img
        self.active_img = active_img
        self.pause = False

    def update(self, *args, **kwargs) -> None:
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            self.clicked(args[0].pos)
        if self.pause:
            self.image = self.pause_img
        else:
            self.image = self.active_img

    def clicked(self, pos):
        pass


class PauseButton(OnOffButton):
    pause_img = load_image("icons\\pause_button.png")
    active_img = load_image("icons\\resume_button.png")

    def __init__(self, name, x, y, *group):
        super(PauseButton, self).__init__(name, PauseButton.pause_img, PauseButton.active_img, x, y, *group)

    def clicked(self, pos):
        if self.is_clicked(pos):
            self.pause = not self.pause


class SoundOnButton(OnOffButton):
    pause_img = load_image("icons\\sound_off_icon.png")
    active_img = load_image("icons\\sound_on_icon.png")

    def __init__(self, name, x, y, *group):
        super(SoundOnButton, self).__init__(name, SoundOnButton.pause_img, SoundOnButton.active_img, x, y, *group)

    def clicked(self, pos):
        if self.is_clicked(pos):
            self.pause = not self.pause
            if self.pause:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()


class Menu:
    def __init__(self, img: pygame.Surface, x, y):
        self.bg = img
        self.rect = pygame.Rect(x, y, *self.bg.get_size())
        self.buttons = pygame.sprite.Group()

    def draw(self, window: pygame.Surface):
        window.blit(self.bg, self.rect.topleft)
        self.buttons.draw(window)


class BuyMenu(Menu):
    def __init__(self):
        super(BuyMenu, self).__init__(load_image("backgrounds\\buy_menu.png"), 0, 0)
        self.rect.y = SCREEN_HEIGHT - self.rect.height
    
    def add_unit(self, unit_name, cost):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        animation = load_image(cur.execute(f"SELECT animation FROM units WHERE name=\"{unit_name}\"").fetchall()[0][0])
        rows, columns = cur.execute(f"SELECT rows, columns FROM units WHERE name=\"{unit_name}\"").fetchall()[0]
        unit_img = cut_sheet(animation, rows, columns)[0]

        btn_size = btn_width, btn_height = 90, 50
        btn_img = pygame.transform.scale(unit_img, btn_size)
        btn_x = self.rect.x + (btn_width + 10) * len(self.buttons.sprites())
        btn_y = self.rect.y + self.rect.height - btn_height
        BuyButton(unit_name, cost, btn_img, btn_x, btn_y, self.buttons)

    def get_clicked(self, pos):
        for btn in self.buttons.sprites():
            if btn.clicked(pos) is not None:
                return btn.clicked(pos)

        return None
