import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_collided(self, pos) -> True:
        return self.rect.collidepoint(*pos)


class BuyButton(Button):
    def __init__(self, img, x, y, cost):
        super(BuyButton, self).__init__(img, x, y)
        self.cost = cost
        font = pygame.font.Font(None, 20)
        cost_text = font.render(str(self.cost), True, (255, 165, 0))
        cost_text_x = self.image.get_width() - cost_text.get_width()
        cost_text_y = self.image.get_height() - cost_text.get_height()
        self.image.blit(cost_text, (cost_text_x, cost_text_y))


class PauseButton(Button):
    def __init__(self, pause_img, active_img, x, y):
        self.pause_img = pause_img
        self.active_img = active_img
        super(PauseButton, self).__init__(self.pause_img, x, y)
        self.pause = False

    def update(self, *args) -> None:
        if self.pause:
            self.image = self.active_img
        else:
            self.image = self.pause_img


class Menu:
    def __init__(self, img: pygame.Surface, x, y):
        self.bg = img
        self.x = x
        self.y = y
        self.width, self.height = self.bg.get_size()
        self.buttons = pygame.sprite.Group()

    def draw(self, window: pygame.Surface):
        self.buttons.draw(self.bg)
        window.blit(self.bg, (self.x, self.y))


class BuyMenu(Menu):
    def add_button(self, btn_img: pygame.Surface, cost: int):
        btn_width, btn_height = 110, 60
        btn_img = pygame.transform.scale(btn_img, (btn_width, btn_height))
        btn_x = self.x + (btn_width + 10) * len(self.buttons.sprites())
        btn_y = self.y + self.height - btn_height
        self.buttons.add(BuyButton(btn_img, btn_x, btn_y, cost))

