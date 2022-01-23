from scripts.constants import *
from scripts.game import Game


class Button(pygame.sprite.Sprite):
    def __init__(self, name, img, x, y):
        super(Button, self).__init__()
        self.name = name
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_clicked(self, pos):
        return self.rect.collidepoint(*pos)


class BuyButton(Button):
    def __init__(self, unit_name, cost, img, x, y):
        super(BuyButton, self).__init__(unit_name, img, x, y)
        self.cost = cost
        font = pygame.font.Font(None, 20)
        cost_text = font.render(str(self.cost), True, ORANGE)
        cost_text_x = self.image.get_width() - cost_text.get_width()
        cost_text_y = self.image.get_height() - cost_text.get_height()
        self.image.blit(cost_text, (cost_text_x, cost_text_y))


class PauseButton(Button):
    def __init__(self, name, pause_img, active_img, x, y):
        super(PauseButton, self).__init__(name, pause_img, x, y)
        self.pause_img = pause_img
        self.active_img = active_img
        self.pause = False

    def update(self, *args) -> None:
        if self.pause:
            self.image = self.active_img
        else:
            self.image = self.pause_img


class Menu:
    def __init__(self, img: pygame.Surface, x, y):
        self.bg = img
        self.rect = pygame.Rect(x, y, *self.bg.get_size())
        self.buttons = pygame.sprite.Group()

    def draw(self, window: pygame.Surface):
        image = self.bg.copy()
        self.buttons.draw(image)
        window.blit(image, *self.rect.topleft)


class BuyMenu(Menu):
    def add_button(self, unit_name, cost, btn_img: pygame.Surface):
        btn_width, btn_height = 110, 60
        btn_img = pygame.transform.scale(btn_img, (btn_width, btn_height))
        btn_x = self.rect.x + (btn_width + 10) * len(self.buttons.sprites())
        btn_y = self.rect.y + self.rect.height - btn_height
        self.buttons.add(BuyButton(unit_name, cost, btn_img, btn_x, btn_y))


class MainMenu(Menu):
    def __init__(self):
        bg = load_image('main_menu\\bg.png')
        super(MainMenu, self).__init__(bg, 0, 0)

        self.logo = load_image('main_menu\\logo.png')

        start_btn_img = load_image('main_menu\\start_button.png')
        start_btn_x = self.rect.width / 2 - start_btn_img.get_width() / 2
        start_btn_y = self.logo.get_height() + 10
        self.start_btn = Button("start button", start_btn_img, start_btn_x, start_btn_y)
        self.buttons.add(self.start_btn)

        self.bg.blit(self.logo, (self.rect.width / 2 - self.logo.get_width() / 2, 0))
        self.buttons.draw(self.bg)

    def run(self, win: pygame.Surface):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if hit start btn

                    if self.start_btn.is_clicked(event.pos):
                        game = Game()
                        game.run(win)
                        running = False
                        print('kdjifjkfk')

            win.fill(pygame.color.Color("black"))
            win.blit(self.bg, self.rect.topleft)
            pygame.display.flip()

        pygame.quit()
