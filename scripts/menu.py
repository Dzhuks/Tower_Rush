from scripts.constants import *


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
        cost_text = font.render(str(self.cost), True, ORANGE)
        cost_text_x = self.image.get_width() - cost_text.get_width()
        cost_text_y = self.image.get_height() - cost_text.get_height()
        self.image.blit(cost_text, (cost_text_x, cost_text_y))
        rect = (0, 0, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(self.image, BLACK, rect, 1)

    def clicked(self, pos):
        if self.is_clicked(pos):
            return self.name, self.cost


class PauseButton(Button):
    def __init__(self, name, x, y, *group):
        self.pause_img = load_image("icons\\pause_button.png")
        self.active_img = load_image("icons\\resume_button.png")
        super(PauseButton, self).__init__(name, self.pause_img, x, y, *group)
        self.pause = False

    def update(self, *args) -> None:
        if self.pause:
            self.image = self.active_img
        else:
            self.image = self.pause_img

    def clicked(self, pos):
        if self.is_clicked(pos):
            self.pause = not self.pause
            print(self.pause)


class Menu:
    def __init__(self, img: pygame.Surface, x, y):
        self.bg = img
        self.rect = pygame.Rect(x, y, *self.bg.get_size())
        self.buttons = pygame.sprite.Group()

    def draw(self, window: pygame.Surface):
        image = self.bg.copy()
        self.buttons.draw(image)
        window.blit(image, self.rect.topleft)


class BuyMenu(Menu):
    def add_button(self, unit_name, cost, unit_img: pygame.Surface):
        btn_width, btn_height = 75, 50
        rect = (unit_img.get_width() / 2 - btn_width / 2, unit_img.get_height() / 2 - btn_height / 2, btn_width, btn_height)
        btn_img = unit_img.subsurface(rect)
        btn_x = self.rect.x + (btn_width + 10) * len(self.buttons.sprites())
        btn_y = self.rect.y + self.rect.height - btn_height
        self.buttons.add(BuyButton(unit_name, cost, btn_img, btn_x, btn_y, self.buttons))

    def get_clicked(self, pos):
        for btn in self.buttons.sprites():
            if btn.clicked(pos) is not None:
                return btn.clicked(pos)

        return None
